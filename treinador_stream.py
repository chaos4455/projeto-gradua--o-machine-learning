import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pandas as pd
import requests
import asyncio
from sklearn.ensemble import RandomForestRegressor
import joblib
from datetime import datetime
import logging
import os
import uuid
import time
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Código executado na inicialização
    asyncio.create_task(treinar_modelo())
    yield
    # Código executado no encerramento (se necessário)

app = FastAPI(title="Treinador", lifespan=lifespan)
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Configuração do CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class EstadoTreinador:
    def __init__(self):
        self.modelo_atual = None
        self.ultima_atualizacao = None
        self.total_treinamentos = 0
        self.total_predicoes = 0
        self.status = "iniciando"

estado = EstadoTreinador()

class PredictRequest(BaseModel):
    idade: int

class PredictResponse(BaseModel):
    predicao: float
    timestamp: str
    modelo_timestamp: str

class StatusResponse(BaseModel):
    status: str
    ultima_atualizacao: str
    total_treinamentos: int
    total_predicoes: int
    modelo_disponivel: bool

INTERVALO_TREINAMENTO = int(os.environ.get("INTERVALO_TREINAMENTO", 60)) # segundos

async def treinar_modelo():
    os.makedirs("modelos", exist_ok=True)
    while True:
        try:
            treinamento_id = str(uuid.uuid4())
            logger.info(f"Treinamento ID: {treinamento_id} - Iniciando treinamento do modelo.")
            logger.info("Tentando conectar ao normalizador em http://localhost:8002")

            # Verificação de status do normalizador
            for attempt in range(3):
                try:
                    logger.info(f"Tentativa {attempt+1}/3 de conexão com o normalizador")
                    status_response = requests.get("http://localhost:8002/status", timeout=5)
                    status_response.raise_for_status()
                    status = status_response.json()
                    if status["status"] == "ativo":
                        logger.info("Conexão com normalizador estabelecida com sucesso")
                        dados_response = requests.get("http://localhost:8002/dados_normalizados", timeout=5)
                        dados_response.raise_for_status()
                        dados_normalizados = dados_response.json()
                        
                        if not dados_normalizados:
                            logger.warning("Nenhum dado normalizado disponível. Aguardando próximo ciclo.")
                            await asyncio.sleep(INTERVALO_TREINAMENTO)
                            continue
                            
                        # Processamento dos dados normalizados
                        df = pd.DataFrame(dados_normalizados)
                        X = df[['idade']].values
                        y = df['salario'].values
                        
                        # Treinamento do modelo
                        modelo = RandomForestRegressor(n_estimators=100, random_state=42)
                        modelo.fit(X, y)
                        
                        # Salvar o modelo
                        modelo_path = os.path.join("modelos", f"modelo_{treinamento_id}.joblib")
                        joblib.dump(modelo, modelo_path)
                        
                        estado.modelo_atual = modelo
                        estado.ultima_atualizacao = datetime.now().isoformat()
                        estado.total_treinamentos += 1
                        
                        logger.info(f"Modelo treinado e salvo com sucesso: {modelo_path}")
                        break
                        
                    logger.warning(f"Normalizador não está ativo. Status atual: {status['status']}")
                    time.sleep(5)
                    
                except requests.exceptions.ConnectionError as e:
                    logger.error(f"Erro de conexão: Verifique se o normalizador está rodando na porta 8002. Detalhes: {str(e)}")
                    time.sleep(5)
                except requests.exceptions.RequestException as e:
                    logger.error(f"Erro ao acessar o normalizador: {str(e)}")
                    time.sleep(5)
            else:
                logger.error("Normalizador indisponível após múltiplas tentativas. Aguardando próximo ciclo.")
                
        except Exception as e:
            logger.exception(f"Erro inesperado durante o treinamento: {str(e)}")
            
        await asyncio.sleep(INTERVALO_TREINAMENTO)

@app.post("/predict")
async def predict(dados: dict):
    try:
        if estado.modelo_atual is None:
            raise HTTPException(
                status_code=503, 
                detail="Modelo ainda não está disponível"
            )
        
        # Validar entrada
        if "idade" not in dados:
            raise HTTPException(
                status_code=400, 
                detail="Campo 'idade' é obrigatório"
            )
            
        idade = dados["idade"]
        
        # Validar tipo e range da idade
        if not isinstance(idade, (int, float)):
            raise HTTPException(
                status_code=400, 
                detail="Idade deve ser um número"
            )
            
        if idade < 0 or idade > 120:
            raise HTTPException(
                status_code=400, 
                detail="Idade deve estar entre 0 e 120 anos"
            )
            
        # Fazer predição
        predicao = estado.modelo_atual.predict([[idade]])[0]
        
        # Incrementar contador de predições
        estado.total_predicoes += 1
        
        # Retornar resultado
        return {
            "predicao": float(predicao),
            "idade": idade,
            "timestamp": datetime.now().isoformat(),
            "modelo_id": estado.ultima_atualizacao
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.exception("Erro durante predição")
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao realizar predição: {str(e)}"
        )

@app.get("/status", response_model=StatusResponse)
async def get_status():
    return {
        "status": "ativo" if estado.modelo_atual is not None else "aguardando",
        "ultima_atualizacao": estado.ultima_atualizacao or datetime.now().isoformat(),
        "total_treinamentos": estado.total_treinamentos,
        "total_predicoes": estado.total_predicoes,
        "modelo_disponivel": estado.modelo_atual is not None
    }

if __name__ == "__main__":
    uvicorn.run("treinador_stream:app", host="0.0.0.0", port=12779, reload=False)
