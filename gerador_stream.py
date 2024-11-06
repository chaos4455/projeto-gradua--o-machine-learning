import uvicorn
from fastapi import FastAPI, HTTPException
from faker import Faker
import pandas as pd
import asyncio
import logging
from datetime import datetime
import random
from pydantic import BaseModel
import os
import uuid

# Configuração de logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = FastAPI(title="Gerador de Dados")

# Configurações do Gerador (tornando configuráveis)
fake = Faker('pt_BR')
TAMANHO_BUFFER = int(os.environ.get("TAMANHO_BUFFER", 15000)) # Aumentando o buffer para 15000
INTERVALO_GERACAO = int(os.environ.get("INTERVALO_GERACAO", 300))  # segundos (5 minutos)

# Carregando dados geográficos do Brasil (substitua pelo seu caminho)
logger.warning("Leitura de shapefile desabilitada conforme solicitação do usuário. Usando dados sintéticos.")
cidades = pd.DataFrame({'cidade': [fake.city() for _ in range(15000)], 'geometry': [None] * 15000})


class EstadoGerador:
    def __init__(self):
        self.dados_atuais = pd.DataFrame()
        self.ultima_geracao = None
        self.total_geracoes = 0
        self.registros_gerados = 0

estado = EstadoGerador()

class StatusResponse(BaseModel):
    status: str
    ultima_geracao: str
    total_geracoes: int
    registros_atuais: int

async def gerar_dados_background():
    while True:
        try:
            geracao_id = str(uuid.uuid4())
            dados = []
            for _ in range(TAMANHO_BUFFER):
                cidade = random.choice(cidades["cidade"])
                # Dados sintéticos de IDH (substitua por dados reais se disponíveis)
                idh = round(random.uniform(0.5, 0.9), 2)  
                
                # Dados geográficos (latitude e longitude aproximadas)
                latitude = None
                longitude = None

                registro = {
                    'nome': fake.name(),
                    'idade': fake.random_int(18, 80),
                    'salario': round(random.uniform(1000, 15000), 2),
                    'cidade': cidade,
                    'estado': fake.state(), # adicionando estado
                    #'regiao': fake.region(), # removendo região
                    'cargo': fake.job(),
                    'idh': idh, # adicionando IDH
                    'latitude': latitude, # adicionando latitude
                    'longitude': longitude, # adicionando longitude
                    'timestamp': datetime.now().isoformat(),
                    'geracao_id': geracao_id
                }
                dados.append(registro)

            estado.dados_atuais = pd.DataFrame(dados)
            estado.ultima_geracao = datetime.now().isoformat()
            estado.total_geracoes += 1
            estado.registros_gerados += len(dados)

            logger.info(f"Geração ID: {geracao_id}, Gerados {len(dados)} novos registros. Tamanho do buffer: {TAMANHO_BUFFER}, Intervalo de geração: {INTERVALO_GERACAO} segundos. Total de registros gerados: {estado.registros_gerados}")

        except Exception as e:
            logger.exception(f"Erro na geração de dados: {str(e)}") # Log com traceback

        await asyncio.sleep(INTERVALO_GERACAO)

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(gerar_dados_background())

@app.get("/dados")
async def get_dados():
    if estado.dados_atuais.empty:
        raise HTTPException(status_code=503, detail="Dados ainda não gerados")
    return estado.dados_atuais.to_dict(orient='records')

@app.get("/status", response_model=StatusResponse)
async def get_status():
    return {
        "status": "ativo",
        "ultima_geracao": estado.ultima_geracao or datetime.now().isoformat(),
        "total_geracoes": estado.total_geracoes,
        "registros_atuais": estado.registros_gerados
    }

if __name__ == "__main__":
    uvicorn.run("gerador_stream:app", host="0.0.0.0", port=8001, reload=False)
