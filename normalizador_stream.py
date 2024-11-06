import uvicorn
from fastapi import FastAPI, HTTPException
import pandas as pd
import requests
import asyncio
from sklearn.preprocessing import StandardScaler
import logging
from datetime import datetime
from pydantic import BaseModel
import os
import uuid
import time

app = FastAPI(title="Normalizador")
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

class EstadoNormalizador:
    def __init__(self):
        self.dados_normalizados = pd.DataFrame()
        self.scaler = StandardScaler()
        self.ultima_normalizacao = None
        self.total_normalizacoes = 0
        self.registros_processados = 0

estado = EstadoNormalizador()

class StatusResponse(BaseModel):
    status: str
    ultima_normalizacao: str
    total_normalizacoes: int
    registros_processados: int

INTERVALO_NORMALIZACAO = int(os.environ.get("INTERVALO_NORMALIZACAO", 60)) # segundos

async def coletar_e_normalizar():
    while True:
        try:
            normalizacao_id = str(uuid.uuid4())
            logger.info(f"Normalização ID: {normalizacao_id} - Iniciando coleta e normalização de dados.")

            # Verificação de status do gerador
            for attempt in range(3):
                try:
                    status_response = requests.get("http://localhost:8001/status", timeout=5)
                    status_response.raise_for_status()
                    status = status_response.json()
                    if status["status"] == "ativo":
                        break
                    logger.warning(f"Gerador indisponível. Tentativa {attempt+1}/3. Tentando novamente em 5 segundos...")
                    time.sleep(5)
                except requests.exceptions.RequestException as e:
                    logger.warning(f"Erro ao verificar status do gerador: {e}. Tentando novamente em 5 segundos...")
                    time.sleep(5)
            else:
                logger.error(f"Gerador indisponível após múltiplas tentativas.")
                await asyncio.sleep(INTERVALO_NORMALIZACAO)
                continue

            response = requests.get("http://localhost:8001/dados", timeout=5)
            response.raise_for_status() # Raise HTTPError for bad responses (4xx or 5xx)
            dados = pd.DataFrame(response.json())
            
            colunas_numericas = ['idade', 'salario']
            if not all(col in dados.columns for col in colunas_numericas):
                logger.warning(f"Normalização ID: {normalizacao_id} - Algumas colunas numéricas não encontradas: {set(colunas_numericas) - set(dados.columns)}")
                continue # Pula para a próxima iteração se as colunas não existirem

            # Normaliza apenas as colunas numéricas
            dados_numericos = dados[colunas_numericas]
            dados_normalizados_numericos = estado.scaler.fit_transform(dados_numericos)
            dados[colunas_numericas] = dados_normalizados_numericos
            
            estado.dados_normalizados = dados
            estado.ultima_normalizacao = datetime.now().isoformat()
            estado.total_normalizacoes += 1
            estado.registros_processados = len(dados)
            
            logger.info(f"Normalização ID: {normalizacao_id} - Normalizados {len(dados)} registros. Total de registros processados: {estado.registros_processados}")
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Normalização ID: {normalizacao_id} - Erro ao obter dados do gerador: {e}")
        except Exception as e:
            logger.exception(f"Normalização ID: {normalizacao_id} - Erro na normalização: {str(e)}") # Log com traceback
        
        await asyncio.sleep(INTERVALO_NORMALIZACAO)

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(coletar_e_normalizar())

@app.get("/dados_normalizados")
async def get_dados_normalizados():
    if estado.dados_normalizados.empty:
        raise HTTPException(status_code=503, detail="Dados ainda não normalizados")
    return estado.dados_normalizados.to_dict(orient='records')

@app.get("/status", response_model=StatusResponse)
async def get_status():
    return {
        "status": "ativo" if not estado.dados_normalizados.empty else "aguardando",
        "ultima_normalizacao": estado.ultima_normalizacao or datetime.now().isoformat(),
        "total_normalizacoes": estado.total_normalizacoes,
        "registros_processados": estado.registros_processados
    }

if __name__ == "__main__":
    uvicorn.run("normalizador_stream:app", host="0.0.0.0", port=8002, reload=False)
