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

app = FastAPI(title="Treinador")
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

class EstadoTreinador:
    def __init__(self):
        self.modelo_atual = None
        self.ultima_atualizacao = None
        self.total_treinos = 0
        self.total_predicoes = 0

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
    total_treinos: int
    total_predicoes: int

INTERVALO_TREINAMENTO = int(os.environ.get("INTERVALO_TREINAMENTO", 60)) # segundos

async def treinar_modelo():
    os.makedirs("modelos", exist_ok=True) # Cria o diretório apenas uma vez
    while True:
        try:
            treinamento_id = str(uuid.uuid4())
            logger.info(f"Treinamento ID: {treinamento_id} - Iniciando treinamento do modelo.")
            response = requests.get("http://localhost:8002/dados_normalizados", timeout=5)
            response.raise_for_status() # Raise HTTPError for bad responses (4xx or 5xx)
            dados = pd.DataFrame(response.json())
            
            X = dados[['idade']]
            y = dados['salario']
            
            modelo = RandomForestRegressor(n_estimators=100)
            modelo.fit(X, y)
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            modelo_path = f"modelos/modelo_{timestamp}.joblib"
            
            joblib.dump(modelo, modelo_path)
            
            estado.modelo_atual = modelo
            estado.ultima_atualizacao = timestamp
            estado.total_treinos += 1
            
            logger.info(f"Treinamento ID: {treinamento_id} - Modelo treinado e salvo: {modelo_path}. Registros usados: {len(dados)}")
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Treinamento ID: {treinamento_id} - Erro ao obter dados do normalizador: {e}")
        except Exception as e:
            logger.exception(f"Treinamento ID: {treinamento_id} - Erro no treinamento: {str(e)}") # Log com traceback
            
        await asyncio.sleep(INTERVALO_TREINAMENTO)

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(treinar_modelo())

@app.post("/predict", response_model=PredictResponse)
async def predict(dados: PredictRequest):
    if estado.modelo_atual is None:
        raise HTTPException(status_code=503, detail="Modelo ainda não treinado")
    try:
        predicao = estado.modelo_atual.predict([[dados.idade]])
        estado.total_predicoes += 1
        return {
            "predicao": float(predicao[0]),
            "timestamp": datetime.now().isoformat(),
            "modelo_timestamp": estado.ultima_atualizacao
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/status", response_model=StatusResponse)
async def get_status():
    return {
        "status": "ativo" if estado.modelo_atual else "aguardando",
        "ultima_atualizacao": estado.ultima_atualizacao or datetime.now().isoformat(),
        "total_treinos": estado.total_treinos,
        "total_predicoes": estado.total_predicoes
    }

if __name__ == "__main__":
    uvicorn.run("treinador_stream:app", host="0.0.0.0", port=8003, reload=False)
