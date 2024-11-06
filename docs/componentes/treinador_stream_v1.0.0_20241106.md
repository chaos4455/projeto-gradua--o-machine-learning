# Treinador de Stream de Dados - v1.0.0 (06/11/2024)

**Elias Andrade - Arquiteto de Soluções Replika AI Solutions Maringá - PR**

Este componente treina um modelo de regressão para prever o salário com base na idade, utilizando dados normalizados fornecidos pelo `Normalizador de Stream`. O modelo treinado é um `RandomForestRegressor` do scikit-learn, conhecido por sua robustez e boa performance em diversos cenários.

## Funcionalidades:

* **Coleta de Dados:** Coleta dados normalizados do `Normalizador de Stream` via requisição HTTP para o endpoint `/dados_normalizados`.
* **Treinamento de Modelo:** Treina um modelo `RandomForestRegressor` usando os dados coletados.
* **Persistência de Modelo:** Salva o modelo treinado em disco na pasta `modelos`, com um nome baseado no timestamp.
* **Predição:** Permite fazer previsões de salário com base na idade via endpoint `/predict`.
* **API RESTful:** Exporta previsões via endpoint `/predict` e informações de status via `/status`.
* **Tratamento de Erros:** Inclui tratamento de exceções para lidar com erros de requisição HTTP e erros durante o treinamento.
* **Logging:** Implementa logging detalhado para monitoramento e depuração.
* **Monitoramento de Status:** Fornece informações sobre o status do treinamento, incluindo a última atualização do modelo, o total de treinamentos e o número de predições realizadas.

## Arquitetura:

O componente opera como um consumidor de dados, recebendo dados normalizados do `Normalizador de Stream` e treinando um modelo com esses dados.  Ele utiliza `asyncio` para executar o treinamento em background.

![Diagrama de Arquitetura](diagrama_arquitetura.png)

## Tecnologias Utilizadas:

* **Python:** Linguagem de programação principal.
* **FastAPI:** Framework para criação de APIs RESTful.
* **Requests:** Biblioteca para realizar requisições HTTP.
* **Scikit-learn:** Biblioteca para Machine Learning, usada para o `RandomForestRegressor`.
* **Joblib:** Biblioteca para salvar e carregar modelos de Machine Learning.
* **Pandas:** Biblioteca para manipulação de dados.
* **Asyncio:** Biblioteca para programação assíncrona.
* **Logging:** Para monitoramento e depuração.
* **uvicorn:** Servidor ASGI para executar a aplicação FastAPI.

## Exemplos de Uso:

**Endpoint `/predict`:**  Recebe um JSON com a idade e retorna a predição do salário:

**Request:**

```json
{
  "idade": 30
}
```

**Response:**

```json
{
  "predicao": 5500.5,
  "timestamp": "2024-11-06T10:00:00",
  "modelo_timestamp": "20241106_100000"
}
```

**Endpoint `/status`:** Retorna um JSON com o status do treinador:

```json
{
  "status": "ativo",
  "ultima_atualizacao": "2024-11-06T10:00:00",
  "total_treinos": 3,
  "total_predicoes": 15
}
```

## Considerações:

* A performance pode ser otimizada com o uso de técnicas de otimização de hiperparâmetros.
* A escalabilidade pode ser melhorada com o uso de um sistema de treinamento distribuído.
* A escolha do `RandomForestRegressor` é uma escolha inicial, e outros modelos podem ser explorados para melhorar a precisão.

## Referências:

* [Documentação FastAPI](https://fastapi.tiangolo.com/)
* [Documentação Scikit-learn](https://scikit-learn.org/stable/)
* [Documentação Joblib](https://joblib.readthedocs.io/en/latest/)


## Inspirações:

Este componente foi inspirado na necessidade de criar um sistema de aprendizado de máquina contínuo que se adapta a novos dados em tempo real.  A escolha do `RandomForestRegressor` se deve à sua capacidade de lidar com dados não lineares e sua robustez a outliers.  A arquitetura é inspirada em sistemas de Machine Learning em produção, onde os modelos são treinados periodicamente e as previsões são feitas em tempo real.  A capacidade de salvar e carregar modelos permite a fácil integração com sistemas de monitoramento e gerenciamento de modelos.  A integração com os componentes anteriores demonstra a capacidade de criar pipelines de dados complexos e robustos para aplicações de Machine Learning.
