import uvicorn
from fastapi import FastAPI
import requests
import asyncio
import logging
from datetime import datetime
from pydantic import BaseModel
import random
import uuid

app = FastAPI(title="Consumidor")
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

class EstadoConsumidor:
    def __init__(self):
        self.ultima_predicao = None
        self.total_consumos = 0
        self.ultima_tentativa = None
        self.erros = 0

estado = EstadoConsumidor()

class StatusResponse(BaseModel):
    status: str
    ultima_predicao: float
    total_consumos: int
    ultima_tentativa: str
    erros: int

async def consumir_predicoes():
    while True:
        try:
            consumo_id = str(uuid.uuid4())
            idade = random.randint(18, 80) # Idade aleatória
            estado.ultima_tentativa = datetime.now().isoformat()
            
            logger.info(f"Consumo ID: {consumo_id} - Iniciando consumo de predição para idade {idade}.")
            response = requests.post(
                "http://localhost:8003/predict",
                json={"idade": idade},
                timeout=5
            )
            response.raise_for_status() # Raise HTTPError for bad responses (4xx or 5xx)
            
            resultado = response.json()
            estado.ultima_predicao = resultado['predicao']
            estado.total_consumos += 1
            logger.info(f"Consumo ID: {consumo_id} - Predição realizada para idade {idade}: {resultado}")
            
        except requests.exceptions.RequestException as e:
            estado.erros += 1
            logger.error(f"Consumo ID: {consumo_id} - Erro ao consumir modelo: {e}")
        except Exception as e:
            estado.erros += 1
            logger.exception(f"Consumo ID: {consumo_id} - Erro inesperado ao consumir modelo: {e}")
            
        await asyncio.sleep(60)

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(consumir_predicoes())

@app.get("/status", response_model=StatusResponse)
async def get_status():
    return {
        "status": "ativo",
        "ultima_predicao": estado.ultima_predicao,
        "total_consumos": estado.total_consumos,
        "ultima_tentativa": estado.ultima_tentativa or datetime.now().isoformat(),
        "erros": estado.erros
    }

if __name__ == "__main__":
    uvicorn.run("consumidor_stream:app", host="0.0.0.0", port=8005, reload=False)
