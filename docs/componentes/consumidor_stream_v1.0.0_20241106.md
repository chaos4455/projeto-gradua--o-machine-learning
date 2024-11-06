# Consumidor de Stream de Predições - v1.0.0 (06/11/2024)

**Elias Andrade - Arquiteto de Soluções Replika AI Solutions Maringá - PR**

Este componente consome as predições geradas pelo `Treinador de Stream`, simulando um sistema que utiliza as previsões do modelo em tempo real.  Ele periodicamente envia uma requisição ao `Treinador de Stream` com uma idade aleatória e registra a predição recebida.

## Funcionalidades:

* **Solicitação de Predições:** Envia requisições HTTP para o endpoint `/predict` do `Treinador de Stream`, fornecendo uma idade aleatória como entrada.
* **Registro de Predições:** Registra as predições recebidas, incluindo o timestamp e a predição em si.
* **Tratamento de Erros:** Inclui tratamento de exceções para lidar com erros de requisição HTTP e outros erros durante o consumo.
* **Logging:** Implementa logging detalhado para monitoramento e depuração.
* **Monitoramento de Status:** Fornece informações sobre o status do consumo, incluindo a última predição recebida, o total de consumos, a última tentativa de consumo e o número de erros.
* **API RESTful:** Exporta informações de status via endpoint `/status`.

## Arquitetura:

O componente opera como um consumidor de predições, recebendo previsões do `Treinador de Stream` e registrando-as.  Ele utiliza `asyncio` para executar o consumo em background.

![Diagrama de Arquitetura](diagrama_arquitetura.png)

## Tecnologias Utilizadas:

* **Python:** Linguagem de programação principal.
* **FastAPI:** Framework para criação de APIs RESTful.
* **Requests:** Biblioteca para realizar requisições HTTP.
* **Asyncio:** Biblioteca para programação assíncrona.
* **Logging:** Para monitoramento e depuração.
* **uvicorn:** Servidor ASGI para executar a aplicação FastAPI.

## Exemplos de Uso:

**Endpoint `/status`:** Retorna um JSON com o status do consumidor:

```json
{
  "status": "ativo",
  "ultima_predicao": 6000.2,
  "total_consumos": 12,
  "ultima_tentativa": "2024-11-06T10:00:00",
  "erros": 0
}
```

## Considerações:

* A escalabilidade pode ser melhorada com o uso de um sistema de mensagens assíncronas (como Kafka) para comunicação entre o treinador e o consumidor.
* A adição de um sistema de persistência de dados para as predições consumidas pode ser útil para análise posterior.

## Referências:

* [Documentação FastAPI](https://fastapi.tiangolo.com/)


## Inspirações:

Este componente foi inspirado na necessidade de simular um sistema que utiliza as previsões de um modelo de Machine Learning em tempo real.  A arquitetura é inspirada em sistemas de processamento de eventos, onde os eventos (predições) são consumidos e processados.  A escolha de usar uma idade aleatória demonstra a capacidade de consumir predições para diferentes entradas.  A integração com os componentes anteriores demonstra a capacidade de criar pipelines de dados complexos e robustos para aplicações de Machine Learning.
