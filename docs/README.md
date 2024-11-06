# Sistema de Processamento de Stream de Dados - v1.2.1 (06/11/2024)

**Elias Andrade - Arquiteto de Soluções Replika AI Solutions Maringá - PR**

Este repositório contém um sistema de processamento de stream de dados em tempo real, construído com microserviços FastAPI.  Ele demonstra um pipeline completo: geração, normalização, treinamento e consumo de previsões.

## 1. Visão Geral

Sistema modular e escalável para processamento de dados em tempo real, utilizando microserviços FastAPI.  O pipeline consiste em quatro componentes principais: Gerador de Dados, Normalizador, Treinador e Consumidor.  Cada componente é um microsserviço independente, que pode ser escalado horizontalmente para atender a demandas crescentes.

## 2. Arquitetura

### Diagrama de Arquitetura

```
+-----------------+     +-----------------+     +-----------------+     +-----------------+
| Gerador de Dados |---->| Normalizador    |---->| Treinador      |---->| Consumidor      |
+-----------------+     +-----------------+     +-----------------+     +-----------------+
     ^                                                                        |
     |                                                                        v
     +-----------------------------------------------------------------------+
                                         |
                                         v
                                  Monitoramento e Logs
```

### Descrição da Arquitetura

O pipeline é composto por quatro microsserviços principais:

1. **Gerador de Dados:** Gera dados sintéticos usando `Faker`, simulando um fluxo contínuo. Configurável via variáveis de ambiente `TAMANHO_BUFFER` e `INTERVALO_GERACAO`.  Documentação detalhada em `docs/componentes/gerador_stream.md`.

2. **Normalizador:** Normaliza dados numéricos usando `StandardScaler` do scikit-learn.  Garante consistência para o modelo de Machine Learning.  O intervalo de normalização é configurável via variável de ambiente `INTERVALO_NORMALIZACAO`. Documentação detalhada em `docs/componentes/normalizador_stream.md`.

3. **Treinador:** Treina um modelo `RandomForestRegressor` periodicamente. Salva modelos treinados usando `joblib` na pasta `modelos`. O intervalo de treinamento é configurável via variável de ambiente `INTERVALO_TREINAMENTO`. Documentação detalhada em `docs/componentes/treinador_stream.md`.

4. **Consumidor:** Consome previsões do Treinador, simulando um sistema que utiliza as previsões em tempo real. O intervalo de consumo é definido implicitamente pelo `asyncio.sleep(60)` no código. Documentação detalhada em `docs/componentes/consumidor_stream.md`.


## 3. Tecnologias

* Python 3.7+
* FastAPI
* Scikit-learn
* Faker
* Joblib
* Requests
* Asyncio
* Pydantic

## 4. Como Executar

1. Instalar dependências: `pip install -r requirements.txt`
2. Executar cada componente em um terminal separado (comandos em documentação individual).

## 5. Documentação Detalhada

Disponível na pasta `docs/componentes`.  Cada componente possui sua própria documentação detalhada.

## 6. Considerações Futuras

* Escalabilidade (Kafka)
* Persistência de Dados (PostgreSQL/MySQL)
* Monitoramento
* CI/CD
* Interface Gráfica
* Modelos Alternativos
* Testes

## 7.  Requisitos de Software

Python 3.7+ e as bibliotecas listadas em `requirements.txt`.

## 8.  Instalação

Clonar o repositório e executar `pip install -r requirements.txt`.

## 9.  Execução dos Componentes

Comandos `uvicorn` para cada componente (ver documentação individual).

## 10.  Comunicação entre Componentes

Requisições HTTP.  Simples, eficiente e amplamente utilizado.

## 11.  Modelo de Machine Learning

`RandomForestRegressor`. Robusto e eficiente para dados não lineares.

## 12.  Normalização de Dados

`StandardScaler` do scikit-learn.  Garante dados com média 0 e desvio padrão 1.

## 13.  Geração de Dados Sintéticos

Biblioteca `Faker`.  Gera dados realistas para simulação.

## 14.  Persistência de Modelos

`joblib`.  Permite salvar e carregar modelos treinados rapidamente.

## 15.  Contribuições

Contribuições são bem-vindas! Abra um *issue* ou *pull request*.
