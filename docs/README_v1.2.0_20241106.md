# Sistema de Processamento de Stream de Dados - v1.2.0 (06/11/2024)

**Elias Andrade - Arquiteto de Soluções Replika AI Solutions Maringá - PR**

Este repositório contém um sistema de processamento de stream de dados em tempo real, construído com microserviços FastAPI.  Ele demonstra um pipeline completo: geração, normalização, treinamento e consumo de previsões.

## 1. Visão Geral

Sistema modular e escalável para processamento de dados em tempo real, utilizando microserviços FastAPI.

## 2. Componentes Principais

* Gerador de Dados
* Normalizador
* Treinador
* Consumidor

## 3. Arquitetura

Microserviços comunicando-se via requisições HTTP.  Arquitetura modular e escalável.

## 4. Diagrama de Arquitetura

(Incluir diagrama aqui)

## 5. Gerador de Dados

Gera dados sintéticos usando `Faker`, simulando um fluxo contínuo. Configurável via variáveis de ambiente.

## 6. Normalizador

Normaliza dados numéricos usando `StandardScaler` do scikit-learn.  Garante consistência para o modelo de Machine Learning.

## 7. Treinador

Treina um modelo `RandomForestRegressor` periodicamente. Salva modelos treinados usando `joblib`.

## 8. Consumidor

Consome previsões do Treinador, simulando um sistema que utiliza as previsões em tempo real.

## 9. Tecnologias

* Python 3.7+
* FastAPI
* Scikit-learn
* Faker
* Joblib
* Requests
* Asyncio
* Pydantic

## 10. Como Executar

1. Instalar dependências: `pip install -r requirements.txt`
2. Executar cada componente em um terminal separado (comandos em documentação individual).

## 11. Documentação Detalhada

Disponível na pasta `docs/componentes`.  Cada componente possui sua própria documentação detalhada.

## 12.  Arquitetura Detalhada

Descrita em `docs/arquitetura.md`.  Inclui diagrama e descrição completa.

## 13.  Considerações Futuras

* Escalabilidade (Kafka)
* Persistência de Dados (PostgreSQL/MySQL)
* Monitoramento
* CI/CD
* Interface Gráfica
* Modelos Alternativos
* Testes

## 14.  Requisitos de Software

Python 3.7+ e as bibliotecas listadas em `requirements.txt`.

## 15.  Instalação

Clonar o repositório e executar `pip install -r requirements.txt`.

## 16.  Execução dos Componentes

Comandos `uvicorn` para cada componente (ver documentação individual).

## 17.  Comunicação entre Componentes

Requisições HTTP.  Simples, eficiente e amplamente utilizado.

## 18.  Modelo de Machine Learning

`RandomForestRegressor`. Robusto e eficiente para dados não lineares.

## 19.  Normalização de Dados

`StandardScaler` do scikit-learn.  Garante dados com média 0 e desvio padrão 1.

## 20.  Geração de Dados Sintéticos

Biblioteca `Faker`.  Gera dados realistas para simulação.

## 21.  Persistência de Modelos

`joblib`.  Permite salvar e carregar modelos treinados rapidamente.

## 22.  Contribuições

Contribuições são bem-vindas! Abra um *issue* ou *pull request*.
