# Arquitetura do Sistema de Processamento de Stream de Dados - v1.0.0 (06/11/2024)

**Elias Andrade - Arquiteto de Soluções Replika AI Solutions Maringá - PR**

Este documento descreve a arquitetura do sistema de processamento de stream de dados, que consiste em quatro componentes principais: Gerador, Normalizador, Treinador e Consumidor.  O sistema é projetado para processar dados em tempo real, treinando um modelo de Machine Learning continuamente e fornecendo previsões.

## Diagrama de Arquitetura:

```
+-----------------+     +-----------------+     +-----------------+     +-----------------+
| Gerador de Dados |---->| Normalizador    |---->| Treinador      |---->| Consumidor     |
+-----------------+     +-----------------+     +-----------------+     +-----------------+
      ^                                                                        |
      |                                                                        v
      +-----------------------------------------------------------------------+
                                          |
                                          v
                                   Banco de Dados (SQLite)
```

## Descrição dos Componentes:

* **Gerador de Dados:** Gera dados sintéticos em tempo real, simulando um fluxo contínuo de informações.  Utiliza a biblioteca `Faker` para criar dados realistas.  A frequência de geração é configurável.
* **Normalizador:** Coleta os dados brutos do Gerador, normaliza as colunas numéricas usando `StandardScaler` do scikit-learn, e disponibiliza os dados normalizados para o Treinador.
* **Treinador:** Treina um modelo de regressão `RandomForestRegressor` usando os dados normalizados.  O modelo é treinado periodicamente e salvo em disco.  Disponibiliza um endpoint para realizar previsões.
* **Consumidor:** Consome as previsões do Treinador, simulando um sistema que utiliza as previsões em tempo real.  Solicita previsões com uma idade aleatória e registra os resultados.

## Tecnologias Utilizadas:

* **Python:** Linguagem de programação principal.
* **FastAPI:** Framework para criação de APIs RESTful.
* **Scikit-learn:** Biblioteca para Machine Learning.
* **Faker:** Biblioteca para geração de dados sintéticos.
* **Joblib:** Biblioteca para salvar e carregar modelos.
* **Requests:** Biblioteca para requisições HTTP.
* **Asyncio:** Para programação assíncrona.
* **SQLite:** Banco de dados (embora não utilizado diretamente nos componentes principais, poderia ser usado para persistir dados).

## Fluxo de Dados:

1. O **Gerador** gera dados e os disponibiliza via API.
2. O **Normalizador** coleta os dados do Gerador, normaliza-os e os disponibiliza via API.
3. O **Treinador** coleta os dados normalizados, treina o modelo e salva-o.  Ele também fornece um endpoint para predições.
4. O **Consumidor** solicita predições ao Treinador e registra os resultados.

## Considerações Futuas:

* **Escalabilidade:** Implementar um sistema de mensagens assíncronas (como Kafka) para melhorar a escalabilidade e desacoplar os componentes.
* **Persistência de Dados:** Utilizar um banco de dados para persistir os dados gerados, os dados normalizados e as predições.
* **Monitoramento:** Implementar um sistema de monitoramento para acompanhar a performance de cada componente e o desempenho do modelo.
* **Integração Contínua/Entrega Contínua (CI/CD):** Automatizar o processo de build, teste e deploy do sistema.


## Inspirações:

A arquitetura é inspirada em pipelines de dados modernos, utilizando o conceito de microserviços para criar um sistema modular, escalável e fácil de manter.  A escolha das tecnologias se baseia em sua maturidade, performance e facilidade de uso.  A integração entre os componentes demonstra a capacidade de criar sistemas complexos e robustos para aplicações de Machine Learning em tempo real.  A arquitetura é similar a pipelines de processamento de dados em larga escala, como aqueles usados em empresas de tecnologia como o Google e o Netflix.
