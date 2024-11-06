# Configuração do Pipeline de Processamento de Stream

**Elias Andrade - Arquiteto de Soluções Replika AI Solutions Maringá - PR - 06/11/2024**

Este documento descreve a configuração do pipeline de processamento de stream, definida no arquivo `config.py`.

## Serviços

A configuração define os seguintes serviços:

| Serviço          | Módulo                 | Porta | Atraso de Retorno (segundos) | Tentativas Máximas |
|-----------------|--------------------------|-------|-----------------------------|----------------------|
| Gerador de Dados | `gerador_stream`        | 12777 | 5                           | 3                    |
| Normalizador     | `normalizador_stream`    | 12778 | 5                           | 3                    |
| Treinador        | `treinador_stream`       | 12779 | 5                           | 3                    |
| Consumidor       | `consumidor_stream`      | 12780 | 5                           | 3                    |

Cada serviço é definido por um dicionário com as seguintes chaves:

* `name`: Nome do serviço (string).
* `module`: Nome do módulo Python que contém a implementação do serviço (string).
* `port`: Porta em que o serviço escuta (inteiro).
* `retry_delay`: Atraso em segundos antes de tentar reiniciar o serviço após uma falha (inteiro).
* `max_retries`: Número máximo de tentativas de reinicialização antes de desistir (inteiro).

## Detalhes de Implementação

A configuração é carregada pelo arquivo `main.py` para iniciar e monitorar os serviços.  O uso de um arquivo de configuração separado permite uma fácil modificação e manutenção dos parâmetros do pipeline.

---
💡 **Referência:** A estrutura modular desta configuração me lembra a arquitetura de microsserviços, popularizada por empresas como Netflix e Amazon.  A capacidade de configurar e gerenciar cada serviço individualmente aumenta a flexibilidade e a escalabilidade do sistema.
