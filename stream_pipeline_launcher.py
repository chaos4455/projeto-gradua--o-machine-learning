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

# Configuração dos serviços com novas portas
SERVICES = [
    {
        'name': 'Gerador de Dados',
        'file': 'gerador_stream',
        'port': 12777,
        'process': None,
        'max_retries': 3,
        'retry_delay': 10
    },
    {
        'name': 'Normalizador',
        'file': 'normalizador_stream',
        'port': 12778,
        'process': None,
        'max_retries': 3,
        'retry_delay': 10
    },
    {
        'name': 'Treinador',
        'file': 'treinador_stream',
        'port': 12779,
        'process': None,
        'max_retries': 3,
        'retry_delay': 10
    },
    {
        'name': 'Consumidor',
        'file': 'consumidor_stream',
        'port': 12780,
        'process': None,
        'max_retries': 3,
        'retry_delay': 10
    }
]


def check_port(port):
    """Verifica se a porta está em uso usando sockets"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('localhost', port)) == 0

def start_service(service):
    """Inicia um serviço específico com tratamento de erros e reinicialização"""
    try:
        # Verifica se o arquivo existe antes de tentar executar
        module_path = f"{service['file']}.py"
        if not os.path.exists(module_path):
            logger.error(f"Arquivo {module_path} não encontrado")
            return None

        process = subprocess.Popen(
            ['python', '-m', 'uvicorn', f"{service['file']}:app", '--host', '0.0.0.0', '--port', str(service['port'])],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True
        )
        time.sleep(2)  # Aguarda inicialização
        
        # Verifica se o processo está rodando
        if process.poll() is None:
            logger.info(f"Iniciado {service['name']} na porta {service['port']} (PID: {process.pid})")
            return process
        else:
            logger.error(f"Falha ao iniciar {service['name']}")
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
            response = requests.get("http://localhost:12780/status", timeout=5)
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
        monitor_services() # adicionando monitoramento de serviços
        asyncio.run(monitor_pipeline())
    except KeyboardInterrupt:
        logger.info("Interrupção manual detectada")
        stop_pipeline()
    except Exception as e:
        logger.error(f"Erro não esperado: {str(e)}")
        stop_pipeline()
    finally:
        logger.info("Pipeline finalizado")
