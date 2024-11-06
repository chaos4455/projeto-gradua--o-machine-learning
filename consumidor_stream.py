import uvicorn
from fastapi import FastAPI, HTTPException
import requests
import asyncio
import logging
from datetime import datetime
from pydantic import BaseModel
import random
import uuid
import time

# Configura o logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = FastAPI(title="Consumidor")

class EstadoConsumidor:
    """Armazena o estado do consumidor."""
    def __init__(self):
        self.ultima_predicao = None
        self.total_consumos = 0
        self.ultima_tentativa = None
        self.erros = 0

estado = EstadoConsumidor()

class StatusResponse(BaseModel):
    """Modelo para a resposta de status."""
    status: str
    ultima_predicao: float | None
    total_consumos: int
    ultima_tentativa: str
    erros: int

async def consumir_predicoes():
    """Consome predições do treinador em loop."""
    while True:
        try:
            consumo_id = str(uuid.uuid4())
            idade = random.randint(18, 80)
            estado.ultima_tentativa = datetime.now().isoformat()
            logger.info(f"Consumo ID: {consumo_id} - Iniciando consumo de predição para idade {idade}.")

            # Verifica o status do treinador com tratamento de exceções mais robusto
            treinador_ativo = await verificar_status_treinador()
            if not treinador_ativo:
                logger.error(f"Treinador indisponível após múltiplas tentativas.")
                await asyncio.sleep(60)
                continue

            # Tenta consumir a predição com tratamento de exceções e retry
            resultado = await consumir_predicao(idade, consumo_id)
            if resultado:
                estado.ultima_predicao = resultado['predicao']
                estado.total_consumos += 1
                logger.info(f"Consumo ID: {consumo_id} - Predição realizada para idade {idade}: {resultado}")
            else:
                estado.erros += 1
                logger.error(f"Consumo ID: {consumo_id} - Todas as tentativas falharam.")

        except Exception as e:
            estado.erros += 1
            logger.exception(f"Consumo ID: {consumo_id} - Erro inesperado ao consumir modelo: {e}")

        await asyncio.sleep(60)

async def verificar_status_treinador():
    """Verifica o status do treinador com retry."""
    for attempt in range(3):
        try:
            status_response = requests.get("http://localhost:12779/status", timeout=5)
            status_response.raise_for_status()
            status = status_response.json()
            if status["status"] == "ativo":
                return True
            logger.warning(f"Treinador indisponível. Tentativa {attempt+1}/3. Tentando novamente em 5 segundos...")
            time.sleep(5)
        except requests.exceptions.RequestException as e:
            logger.warning(f"Erro ao verificar status do treinador: {e}. Tentando novamente em 5 segundos...")
            time.sleep(5)
    return False

async def consumir_predicao(idade, consumo_id):
    """Consome a predição do treinador com retry."""
    for attempt in range(3):
        try:
            response = requests.post(
                "http://localhost:12779/predict",
                json={"idade": idade},
                timeout=5
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.warning(f"Consumo ID: {consumo_id} - Tentativa {attempt+1}/3 falhou: {e}. Tentando novamente em 5 segundos...")
            time.sleep(5)
    return None


@app.on_event("startup")
async def startup_event():
    """Inicia a tarefa de consumir predições ao iniciar o aplicativo."""
    asyncio.create_task(consumir_predicoes())

@app.get("/api/status", response_model=StatusResponse)
async def get_status():
    """Retorna o status do consumidor."""
    return {
        "status": "ativo",
        "ultima_predicao": estado.ultima_predicao,
        "total_consumos": estado.total_consumos,
        "ultima_tentativa": estado.ultima_tentativa or datetime.now().isoformat(),
        "erros": estado.erros
    }

if __name__ == "__main__":
    uvicorn.run("consumidor_stream:app", host="0.0.0.0", port=12780, reload=False)
