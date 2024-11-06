# Consumidor de Previsões - Documentação 06/11/2024

**Elias Andrade - Arquiteto de Soluções Replika AI Solutions - Maringá, PR**

Este documento descreve o componente `consumidor_stream.py` do pipeline de predição de salário.  Este componente é o elo final da nossa cadeia, como o consumidor final que utiliza o produto.  Ele é responsável por consumir as previsões geradas pelo modelo treinado.

## Funcionalidade

🤖 O consumidor faz requisições periódicas à API do treinador para obter previsões de salário.  Ele mantém um registro do histórico de previsões, incluindo a última predição, o total de consumos, a última tentativa e o número de erros.  A inspiração veio da capacidade das máquinas de executar tarefas repetitivas com precisão e eficiência, como uma linha de montagem que produz produtos em série.

## Código

```python
# ... (código do consumidor_stream.py) ...
```

## Design

O consumidor segue uma arquitetura simples e robusta, utilizando requisições HTTP para se comunicar com o treinador.  Ele é um microsserviço independente, que pode ser escalado horizontalmente para atender a demandas crescentes.  A inspiração veio da elegância e simplicidade do design modular.

## Considerações

* O intervalo de consumo é definido implicitamente pelo `asyncio.sleep(60)` no código.

## Referências

* [Requests](https://requests.readthedocs.io/en/master/)
