from rich.console import Console
from rich.live import Live
from rich.table import Table
from rich.panel import Panel
from rich.layout import Layout
from rich.text import Text
from rich import box
import requests
import time
from datetime import datetime
import psutil
import os
import asyncio
from typing import Dict
import json

# Configuração inicial
console = Console()

# Emojis e símbolos para status
STATUS_SYMBOLS = {
    'online': '🟢',
    'offline': '🔴',
    'warning': '🟡',
    'processing': '⚡',
    'data': '📊',
    'model': '🤖',
    'error': '❌'
}

# Cores para diferentes estados
COLORS = {
    'online': '[green]',
    'offline': '[red]',
    'warning': '[yellow]',
    'error': '[red]',
    'info': '[blue]',
    'success': '[green]'
}

class ServiceMonitor:
    def __init__(self):
        self.services = {
            'gerador': {'port': 8001, 'status': 'offline', 'last_data': None, 'metrics': {}},
            'normalizador': {'port': 8002, 'status': 'offline', 'last_data': None, 'metrics': {}},
            'treinador': {'port': 8003, 'status': 'offline', 'last_data': None, 'metrics': {}},
            'consumidor': {'port': 8005, 'status': 'offline', 'last_data': None, 'metrics': {}}
        }
        self.last_update = datetime.now()

    async def check_service(self, name: str, port: int) -> None:
        """Verifica o status de um serviço específico"""
        try:
            url = f"http://localhost:{port}/status"
            response = requests.get(url, timeout=2)
            response.raise_for_status()
            data = response.json()
            self.services[name]['status'] = 'online'
            self.services[name]['last_data'] = data
            self.services[name]['metrics'] = data
            
        except requests.exceptions.RequestException as e:
            self.services[name]['status'] = 'offline'
            self.services[name]['metrics'] = {}
            print(f"Erro ao acessar {url}: {e}")

    def create_status_table(self) -> Table:
        """Cria tabela de status dos serviços"""
        table = Table(box=box.ROUNDED, title="🔄 Pipeline de Streaming Status", 
                     title_style="bold cyan", expand=True)
        
        table.add_column("Serviço", style="cyan", justify="left")
        table.add_column("Status", justify="center")
        table.add_column("Porta", justify="center")
        table.add_column("Métricas", justify="left", max_width=60) # Limita a largura
        table.add_column("Última Atualização", justify="right")

        for service_name, info in self.services.items():
            status_emoji = STATUS_SYMBOLS.get(info['status'], '⚪')
            metrics_str = self.format_metrics(info['metrics'])
            
            table.add_row(
                f"{service_name.title()}",
                f"{status_emoji} {info['status'].upper()}",
                str(info['port']),
                metrics_str,
                datetime.now().strftime("%H:%M:%S")
            )

        return table

    def create_system_panel(self) -> Panel:
        """Cria painel com informações do sistema"""
        cpu_percent = psutil.cpu_percent()
        memory = psutil.virtual_memory()
        
        system_info = [
            f"CPU: {'🔥' if cpu_percent > 80 else '💻'} {cpu_percent}%",
            f"RAM: {'⚠️' if memory.percent > 80 else '🎯'} {memory.percent}%",
            f"Tempo Online: {self.format_uptime()}",
        ]
        
        return Panel(
            "\n".join(system_info),
            title="🖥️ Sistema",
            border_style="blue",
            padding=(1, 2)
        )

    def format_metrics(self, metrics: Dict) -> str:
        """Formata as métricas para exibição"""
        if not metrics:
            return "Sem dados"
        
        # Limita o número de métricas exibidas
        metrics_to_show = dict(list(metrics.items())[:22])
        
        return " | ".join([f"{k}: {v}" for k, v in metrics_to_show.items()])

    def format_uptime(self) -> str:
        """Calcula e formata o tempo de execução"""
        delta = datetime.now() - self.last_update
        hours, remainder = divmod(int(delta.total_seconds()), 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"

    async def update_services(self) -> None:
        """Atualiza o status de todos os serviços"""
        for service_name, info in self.services.items():
            await self.check_service(service_name, info['port'])

    def create_layout(self) -> Layout:
        """Cria o layout principal da interface"""
        layout = Layout()
        
        layout.split(
            Layout(name="header", size=3),
            Layout(name="main"),
            Layout(name="footer", size=5)
        )
        
        # Header
        layout["header"].update(Panel(
            Text("Monitor de Pipeline de Streaming", style="bold white", justify="center"),
            style="cyan"
        ))
        
        # Main content
        layout["main"].update(self.create_status_table())
        
        # Footer
        layout["footer"].update(self.create_system_panel())
        
        return layout

async def main():
    monitor = ServiceMonitor()
    
    with Live(monitor.create_layout(), refresh_per_second=1, screen=True) as live:
        while True:
            await monitor.update_services()
            live.update(monitor.create_layout())
            await asyncio.sleep(1)

if __name__ == "__main__":
    try:
        console.clear()
        console.print("[bold green]Iniciando Monitor de Pipeline...[/bold green]")
        asyncio.run(main())
    except KeyboardInterrupt:
        console.print("[bold red]Monitor finalizado pelo usuário.[/bold red]")
    except Exception as e:
        console.print(f"[bold red]Erro: {str(e)}[/bold red]")
