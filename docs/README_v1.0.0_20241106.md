# Sistema de Processamento de Stream de Dados - v1.0.0 (06/11/2024)

**Elias Andrade - Arquiteto de Soluções Replika AI Solutions Maringá - PR**

Este repositório contém o código para um sistema de processamento de stream de dados que demonstra a construção de um pipeline de dados em tempo real, incluindo a geração de dados, normalização, treinamento de um modelo de Machine Learning e consumo de previsões.

## Visão Geral:

O sistema consiste em quatro componentes principais, cada um implementado como um serviço FastAPI:

* **Gerador de Dados:** Gera dados sintéticos em tempo real.
* **Normalizador:** Normaliza os dados numéricos.
* **Treinador:** Treina um modelo de regressão `RandomForestRegressor`.
* **Consumidor:** Consome as previsões do modelo treinado.

Cada componente é independente e se comunica via requisições HTTP.  A arquitetura é modular e escalável, permitindo a adição de novos componentes e funcionalidades no futuro.

## Diagrama de Arquitetura:

(Incluir aqui o diagrama de arquitetura, possivelmente uma imagem)

## Como Executar:

1. **Requisitos:** Certifique-se de ter o Python 3.7+ e as bibliotecas listadas em `requirements.txt` instaladas.
2. **Instalação:** Execute `pip install -r requirements.txt`.
3. **Execução:** Execute cada componente em um terminal separado:
    * `uvicorn gerador_stream:app --host 0.0.0.0 --port 8001`
    * `uvicorn normalizador_stream:app --host 0.0.0.0 --port 8002`
    * `uvicorn treinador_stream:app --host 0.0.0.0 --port 8003`
    * `uvicorn consumidor_stream:app --host 0.0.0.0 --port 8005`

## Documentação:

A documentação detalhada de cada componente pode ser encontrada na pasta `docs/componentes`.  A arquitetura geral do sistema é descrita em `docs/arquitetura.md`.

## Tecnologias Utilizadas:

* **Python:** Linguagem de programação principal.
* **FastAPI:** Framework para APIs RESTful.
* **Scikit-learn:** Biblioteca para Machine Learning.
* **Faker:** Biblioteca para geração de dados sintéticos.
* **Joblib:** Biblioteca para salvar e carregar modelos.
* **Requests:** Biblioteca para requisições HTTP.
* **Asyncio:** Para programação assíncrona.

## Contribuições:

Contribuições são bem-vindas!  Por favor, abra um *issue* ou *pull request* se você tiver alguma sugestão ou correção.

## Licença:

(Incluir aqui a licença do projeto)


## Inspirações:

Este projeto foi inspirado pela necessidade de demonstrar a construção de um pipeline de dados em tempo real utilizando tecnologias modernas.  A arquitetura é inspirada em sistemas de processamento de dados em larga escala, como aqueles usados em empresas de tecnologia.  A escolha das tecnologias se baseia em sua maturidade, performance e facilidade de uso.  O projeto demonstra a capacidade de criar sistemas complexos e robustos para aplicações de Machine Learning em tempo real, utilizando conceitos de microserviços e programação assíncrona.  A modularidade do sistema permite fácil expansão e manutenção.
