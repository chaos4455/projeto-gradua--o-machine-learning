import subprocess
import time
import logging
from datetime import datetime
import os
from multiprocessing import Process
import signal
import sys
import asyncio
import requests
import socket

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(f'pipeline_logs_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger('StreamPipelineLauncher')

# Configuração dos serviços
SERVICES = [
    {
        'name': 'Gerador de Dados',
        'file': 'gerador_stream.py',
        'port': 8001,
        'process': None,
        'max_retries': 3,
        'retry_delay': 10
    },
    {
        'name': 'Normalizador',
        'file': 'normalizador_stream.py',
        'port': 8002,
        'process': None,
        'max_retries': 3,
        'retry_delay': 10
    },
    {
        'name': 'Treinador',
        'file': 'treinador_stream.py',
        'port': 8003,
        'process': None,
        'max_retries': 3,
        'retry_delay': 10
    },
    {
        'name': 'Consumidor',
        'file': 'consumidor_stream.py',
        'port': 8005,
        'process': None,
        'max_retries': 3,
        'retry_delay': 10
    }
]


def check_port(port):
    """Verifica se a porta está em uso usando sockets"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('localhost', port)) == 0

def start_service(service, retry_count=0):
    """Inicia um serviço específico com tratamento de erros e reinicialização"""
    try:
        if check_port(service['port']):
            if retry_count < service['max_retries']:
                logger.warning(f"Porta {service['port']} ocupada. Tentativa {retry_count+1} de {service['max_retries']} para iniciar {service['name']}. Tentando novamente em {service['retry_delay']} segundos...")
                time.sleep(service['retry_delay'])
                return start_service(service, retry_count + 1)
            else:
                logger.error(f"Porta {service['port']} ocupada. Número máximo de tentativas excedido para iniciar {service['name']}")
                return None

        process = subprocess.Popen(
            ['python', service['file']],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True
        )
        logger.info(f"Iniciado {service['name']} na porta {service['port']} (PID: {process.pid})")
        return process
    except FileNotFoundError:
        logger.error(f"Arquivo {service['file']} não encontrado!")
        return None
    except Exception as e:
        logger.error(f"Erro ao iniciar {service['name']}: {str(e)}")
        return None

def stop_service(service):
    """Para um serviço específico"""
    if service['process']:
        try:
            service['process'].terminate()
            service['process'].wait(timeout=5)
            logger.info(f"Serviço {service['name']} finalizado")
        except subprocess.TimeoutExpired:
            service['process'].kill()
            logger.warning(f"Forçando finalização do serviço {service['name']}")
        except Exception as e:
            logger.error(f"Erro ao parar o serviço {service['name']}: {e}")
        service['process'] = None

def start_pipeline(wait_time=5):
    """Inicia todo o pipeline"""
    logger.info("Iniciando Pipeline de Streaming...")
    if not os.path.exists('modelos'):
        os.makedirs('modelos')
        logger.info("Diretório 'modelos' criado")
    for service in SERVICES:
        service['process'] = start_service(service)
        time.sleep(wait_time)

def stop_pipeline():
    """Para todo o pipeline"""
    logger.info("Finalizando Pipeline de Streaming...")
    for service in reversed(SERVICES):
        stop_service(service)

def signal_handler(signum, frame):
    """Manipulador de sinais para parada graciosa"""
    logger.info("Sinal de interrupção recebido. Iniciando parada graciosa...")
    stop_pipeline()
    sys.exit(0)

def monitor_services():
    """Monitora os serviços e reinicia se necessário"""
    while True:
        for service in SERVICES:
            if service['process'] and service['process'].poll() is not None:
                logger.warning(f"{service['name']} caiu! Tentando reiniciar...")
                service['process'] = start_service(service)
        time.sleep(10)

async def monitor_pipeline():
    while True:
        try:
            response = requests.get("http://localhost:8005/status", timeout=5)
            response.raise_for_status() # Raise HTTPError for bad responses (4xx or 5xx)
            status = response.json()
            logger.info(f"Último consumo: {status['ultima_predicao']} em {status['ultima_tentativa']}")
        except requests.exceptions.RequestException as e:
            logger.error(f"Erro ao monitorar pipeline: {e}")
        except KeyError as e:
            logger.error(f"Resposta do consumidor inválida: {e}")
        except Exception as e:
            logger.exception(f"Erro inesperado ao monitorar pipeline: {e}")
        await asyncio.sleep(60)

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    try:
        start_pipeline()
        asyncio.run(monitor_pipeline())
    except KeyboardInterrupt:
        logger.info("Interrupção manual detectada")
        stop_pipeline()
    except Exception as e:
        logger.error(f"Erro não esperado: {str(e)}")
        stop_pipeline()
    finally:
        logger.info("Pipeline finalizado")
