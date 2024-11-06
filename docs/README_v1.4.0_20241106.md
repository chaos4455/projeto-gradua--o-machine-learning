# Projeto Pipeline de Processamento de Stream - Documentação v1.4.0 (06/11/2024)

**Elias Andrade - Arquiteto de Soluções Replika AI Solutions Maringá - PR**

Este documento descreve a arquitetura e o funcionamento do pipeline de processamento de stream.  O projeto utiliza Python com `asyncio` para executar um pipeline assíncrono, processando dados em tempo real.

## Visão Geral

O pipeline consiste nos seguintes componentes:

* **Gerador de Stream:**  `(gerador_stream.py)` Responsável por gerar o fluxo de dados.
* **Normalizador de Stream:** `(normalizador_stream.py)` Normaliza os dados recebidos do gerador.
* **Consumidor de Stream:** `(consumidor_stream.py)` Consome os dados normalizados e realiza o processamento final.
* **Treinador de Stream:** `(treinador_stream.py)` Treina um modelo de machine learning com os dados processados.
* **Avaliador de Modelo:** `(avaliador_modelo.py)` Avalia a performance do modelo treinado.
* **Extrator de Logs:** `(extrator_logs.py)` Extrai informações relevantes dos logs do pipeline.
* **Monitor de Serviços:** `(service_monitor.py)` Monitora o status dos serviços do pipeline.
* **Lançador do Pipeline:** `(stream_pipeline_launcher.py)` Inicia e gerencia o pipeline.

## Funcionamento

O arquivo `main.py` é o ponto de entrada do pipeline. Ele inicia os serviços configurados em `config.py` e inicia um monitor de serviços que verifica periodicamente o status de cada serviço.  O pipeline continua em execução até ser interrompido manualmente.

```python
# Exemplo simplificado do main.py
import asyncio

async def run_pipeline():
    # Inicia os serviços
    # ...
    
    # Inicia o monitoramento
    # ...
    
    try:
        while True:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        # ...
```

## Configuração dos Serviços (`config.py`)

O arquivo `config.py` define a lista de serviços que compõem o pipeline. Cada serviço é configurado com as seguintes propriedades:

* `name`: Nome do serviço.
* `module`: Módulo Python que implementa o serviço.
* `port`: Porta em que o serviço escuta.
* `retry_delay`: Atraso em segundos antes de tentar reiniciar o serviço em caso de falha.
* `max_retries`: Número máximo de tentativas de reinicialização.

```python
SERVICES = [
    {'name': 'Gerador de Dados', 'module': 'gerador_stream', 'port': 12777, 'retry_delay': 5, 'max_retries': 3},
    {'name': 'Normalizador', 'module': 'normalizador_stream', 'port': 12778, 'retry_delay': 5, 'max_retries': 3},
    {'name': 'Treinador', 'module': 'treinador_stream', 'port': 12779, 'retry_delay': 5, 'max_retries': 3},
    {'name': 'Consumidor', 'module': 'consumidor_stream', 'port': 12780, 'retry_delay': 5, 'max_retries': 3}
]
```

## Tecnologias Utilizadas

* **Python:** Linguagem de programação principal.
* **Asyncio:** Para processamento assíncrono.
* **Loguru:** Para logging.
* **Scikit-learn (provavelmente):** Para o treinamento do modelo (a confirmar).


## Próximos Passos

* Detalhar o funcionamento de cada componente do pipeline.
* Adicionar diagramas de arquitetura.
* Incluir métricas de performance.
* Documentar o `service_monitor.py`.


## Referências

* [Link para documentação do Asyncio](https://docs.python.org/3/library/asyncio.html)
* [Link para documentação do Loguru](https://loguru.readthedocs.io/en/stable/)


---

**Observações:** Esta documentação é uma versão inicial e será expandida com mais detalhes em futuras atualizações.  A inspiração para este projeto veio da complexidade e elegância de sistemas distribuídos como o Kubernetes, buscando a mesma robustez e escalabilidade em um contexto mais específico.  A escolha de `asyncio` reflete a busca por performance e eficiência no processamento de streams de dados, semelhante à abordagem utilizada em sistemas de alta performance como os usados em jogos online.
