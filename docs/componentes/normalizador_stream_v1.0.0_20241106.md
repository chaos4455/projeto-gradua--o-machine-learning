# Normalizador de Stream de Dados - v1.0.0 (06/11/2024)

**Elias Andrade - Arquiteto de Soluções Replika AI Solutions Maringá - PR**

Este componente é responsável por normalizar os dados brutos gerados pelo `Gerador de Stream`. Ele utiliza o `StandardScaler` do scikit-learn para realizar a normalização, transformando os dados numéricos em uma distribuição com média 0 e desvio padrão 1.

## Funcionalidades:

* **Coleta de Dados:** Coleta dados do `Gerador de Stream` via requisição HTTP para o endpoint `/dados`.
* **Normalização de Dados:** Normaliza as colunas numéricas (`idade` e `salario`) usando `StandardScaler`.
* **API RESTful:** Exporta os dados normalizados via endpoint `/dados_normalizados` e informações de status via `/status`.
* **Tratamento de Erros:** Inclui tratamento de exceções para lidar com erros de requisição HTTP e erros durante a normalização.
* **Logging:** Implementa logging detalhado para monitoramento e depuração.
* **Monitoramento de Status:** Fornece informações sobre o status da normalização, incluindo a última normalização realizada, o total de normalizações e o número de registros processados.

## Arquitetura:

O componente opera como um consumidor de dados, recebendo dados do `Gerador de Stream` e processando-os.  Ele utiliza `asyncio` para executar a coleta e normalização em background.

![Diagrama de Arquitetura](diagrama_arquitetura.png)

## Tecnologias Utilizadas:

* **Python:** Linguagem de programação principal.
* **FastAPI:** Framework para criação de APIs RESTful.
* **Requests:** Biblioteca para realizar requisições HTTP.
* **Scikit-learn:** Biblioteca para Machine Learning, usada para o `StandardScaler`.
* **Pandas:** Biblioteca para manipulação de dados.
* **Asyncio:** Biblioteca para programação assíncrona.
* **Logging:** Para monitoramento e depuração.
* **uvicorn:** Servidor ASGI para executar a aplicação FastAPI.

## Exemplos de Uso:

**Endpoint `/dados_normalizados`:** Retorna um JSON com os dados normalizados:

```json
[
  {
    "nome": "Nome Completo",
    "idade": -0.5,
    "salario": 1.2,
    "cidade": "Cidade",
    "cargo": "Cargo",
    "timestamp": "2024-11-06T10:00:00",
    "geracao_id": "uuid"
  },
  // ... mais dados
]
```

**Endpoint `/status`:** Retorna um JSON com o status do normalizador:

```json
{
  "status": "ativo",
  "ultima_normalizacao": "2024-11-06T10:00:00",
  "total_normalizacoes": 5,
  "registros_processados": 5000
}
```

## Considerações:

* A performance pode ser otimizada com o uso de técnicas de processamento paralelo ou distribuído.
* A escalabilidade pode ser melhorada com o uso de um sistema de mensagens assíncronas (como Kafka) para comunicação entre o gerador e o normalizador.

## Referências:

* [Documentação FastAPI](https://fastapi.tiangolo.com/)
* [Documentação Scikit-learn](https://scikit-learn.org/stable/)


## Inspirações:

A inspiração para este componente vem da necessidade de pré-processar dados em tempo real para modelos de Machine Learning. A normalização é uma etapa crucial no pré-processamento de dados, garantindo que os recursos tenham uma escala similar, evitando que recursos com valores maiores dominem o modelo.  A escolha do `StandardScaler` se deve à sua eficiência e ampla utilização em diversas aplicações de Machine Learning.  A arquitetura é inspirada em pipelines de dados modernos, onde os dados são processados em etapas sequenciais.  A integração com o `Gerador de Stream` demonstra a capacidade de criar pipelines de dados complexos e robustos.
