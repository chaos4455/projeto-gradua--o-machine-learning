import asyncio
from loguru import logger
from config import SERVICES
from service_monitor import ServiceMonitor
from service_launcher import start_service

async def run_pipeline():
    """Executa o pipeline completo"""
    monitor = ServiceMonitor()
    
    # Inicia os serviços
    for service in SERVICES:
        process = start_service(service)
        if process is None:
            logger.error(f"Falha ao iniciar {service['name']}")
            return
        
    # Inicia o monitoramento
    monitor_task = asyncio.create_task(monitor.check_services())
    
    try:
        while True:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        logger.info("Encerrando pipeline...")
        monitor_task.cancel()
        stop_pipeline()

if __name__ == "__main__":
    asyncio.run(run_pipeline())