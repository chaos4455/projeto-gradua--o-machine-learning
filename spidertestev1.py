import requests
import time
import os
import json
import yaml
import matplotlib.pyplot as plt
import seaborn as snsw
import pandas as pd
from datetime import datetime
import uuid
import logging
from pathlib import Path
import numpy as np
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TimeElapsedColumn, track
from rich.panel import Panel
from rich import print as rprint
from colorama import init, Fore, Style

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('SpiderTest')

# Inicialização do colorama e rich console
init()
console = Console()

class SpiderTest:
    def __init__(self, num_iterations=10):
        self.base_url = "http://localhost:12779"  # URL do treinador
        self.test_id = str(uuid.uuid4())
        self.report_dir = self._create_report_dir()
        self.metrics_history = []
        self.console = Console()
        self.num_iterations = num_iterations

    def _create_report_dir(self):
        """Cria diretório para relatórios"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_dir = Path(f"report/test_run_{timestamp}_{self.test_id}")
        report_dir.mkdir(parents=True, exist_ok=True)
        return report_dir

    def _save_metrics(self, metrics, format_type):
        """Salva métricas em diferentes formatos"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Adiciona emojis aos nomes dos arquivos
        format_icons = {
            'json': '📋',
            'yaml': '📝',
            'txt': '📄',
            'md': '📑'
        }
        
        try:
            filepath = self.report_dir / f"metrics_{timestamp}.{format_type}"
            if format_type == 'json':
                with open(filepath, 'w') as f:
                    json.dump(metrics, f, indent=4)
            elif format_type == 'yaml':
                with open(filepath, 'w') as f:
                    yaml.dump(metrics, f)
            elif format_type == 'txt':
                with open(filepath, 'w') as f:
                    for key, value in metrics.items():
                        f.write(f"{key}: {value}\n")
            elif format_type == 'md':
                with open(filepath, 'w') as f:
                    f.write("# Métricas de Teste do Modelo\n\n")
                    for key, value in metrics.items():
                        f.write(f"## {key}\n")
                        f.write(f"{value}\n\n")
            self.console.print(f"{format_icons.get(format_type, '📁')} Métricas salvas em: {filepath}", style="green")
        except Exception as e:
            self.console.print(f"[red]❌ Erro ao salvar {format_type}: {str(e)}[/red]")

    def _generate_plots(self, predictions, actual_values):
        """Gera e salva gráficos"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        plots_dir = self.report_dir / "graficos"
        plots_dir.mkdir(parents=True, exist_ok=True)

        # Gráfico de dispersão
        plt.figure(figsize=(10, 6))
        plt.scatter(actual_values, predictions, alpha=0.5)
        plt.plot([min(actual_values), max(actual_values)], 
                [min(actual_values), max(actual_values)], 
                'r--', lw=2)
        plt.xlabel('Valores Reais')
        plt.ylabel('Predições')
        plt.title('Predições vs Valores Reais')
        plt.savefig(plots_dir / f"scatter_plot_{timestamp}.png")
        plt.close()

        # Gráfico de resíduos
        residuals = np.array(predictions) - np.array(actual_values)
        plt.figure(figsize=(10, 6))
        sns.histplot(residuals, kde=True)
        plt.xlabel('Resíduos')
        plt.ylabel('Frequência')
        plt.title('Distribuição dos Resíduos')
        plt.savefig(plots_dir / f"residuals_{timestamp}.png")
        plt.close()

    def run_test(self):
        """Executa o teste do modelo"""
        try:
            # Gerando dados de teste (mais robusto)
            test_ages = np.random.randint(18, 80, size=10)
            test_results = []
            
            # Realizando predições
            for age in test_ages:
                response = requests.post(
                    f"{self.base_url}/predict",
                    json={"idade": int(age)}
                )
                if response.status_code == 200:
                    prediction = response.json()
                    test_results.append({
                        "idade": age,
                        "predicao": prediction["predicao"],
                        "timestamp": prediction["timestamp"]
                    })
                else:
                    self.console.print(f"[red]❌ Erro na requisição: {response.status_code} - {response.text}[/red]")
                    return
            
            # Calculando métricas
            predictions = np.array([r["predicao"] for r in test_results])
            actual_values = np.array([age * 1000 for age in test_ages])
            
            metrics = {
                "timestamp": datetime.now().isoformat(),
                "idade_testada": test_ages.tolist(),
                "predicao": predictions.tolist(),
                "valor_real": actual_values.tolist(),
                "mse": mean_squared_error(actual_values, predictions),
                "rmse": np.sqrt(mean_squared_error(actual_values, predictions)),
                "mae": mean_absolute_error(actual_values, predictions),
                "r2": r2_score(actual_values, predictions)
            }
            
            # Exibe resumo do resultado
            self.console.print(Panel.fit(
                f"""✨ Resultado do Teste:
                🎯 Idades Testadas: {metrics['idade_testada']}
                🤖 Predições: {metrics['predicao']}
                📊 Valores Reais: {metrics['valor_real']}
                MSE: {metrics['mse']:.2f}
                RMSE: {metrics['rmse']:.2f}
                MAE: {metrics['mae']:.2f}
                R²: {metrics['r2']:.2f}""",
                style="bold green"
            ))
            
            self._save_metrics(metrics, 'json')
            self._save_metrics(metrics, 'yaml')
            self._save_metrics(metrics, 'txt')
            self._save_metrics(metrics, 'md')
            self._generate_plots(predictions, actual_values)
            
        except requests.exceptions.RequestException as e:
            self.console.print(f"[red]❌ Erro de requisição: {e}[/red]")
        except Exception as e:
            self.console.print(f"[red]❌ Erro durante o teste: {str(e)}[/red]")

    def run_tests(self):
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TimeElapsedColumn(),
            console=self.console
        ) as progress:
            for i in range(self.num_iterations):
                task = progress.add_task(f"Teste {i+1}", total=1)
                self.run_test()
                progress.update(task, advance=1)
                time.sleep(1)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='Executa testes no modelo.')
    parser.add_argument('--iterations', type=int, default=10, help='Número de iterações dos testes.')
    args = parser.parse_args()
    spider = SpiderTest(args.iterations)
    spider.run_tests()
