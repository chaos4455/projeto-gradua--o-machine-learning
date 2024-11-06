# Arquitetura do Pipeline de Predição de Salário - 06/11/2024

**Elias Andrade - Arquiteto de Soluções Replika AI Solutions - Maringá, PR**

Este documento descreve a arquitetura do pipeline de predição de salário, um sistema distribuído e modular que utiliza microsserviços para processar dados em tempo real e gerar previsões de salário com base na idade.  A inspiração para esta arquitetura veio da complexidade e beleza de um ecossistema natural, onde diferentes organismos interagem de forma harmoniosa e eficiente.

## Visão Geral

O pipeline é composto por quatro microsserviços principais:

1. **Gerador de Dados:**  Responsável por gerar dados sintéticos, simulando informações realistas de indivíduos.  Este serviço é a base do nosso pipeline, como a semente que dá origem a uma grande árvore.  Ele utiliza a biblioteca `Faker` para gerar dados aleatórios, mas com uma estrutura que imita dados reais.

2. **Normalizador de Dados:**  Normaliza os dados gerados pelo gerador, preparando-os para o treinamento do modelo de machine learning.  Este serviço é crucial para o sucesso do nosso modelo, como a base sólida de uma construção.  Ele utiliza o `StandardScaler` do scikit-learn para garantir que todas as features tenham a mesma escala.

3. **Treinador de Modelo:**  Treina um modelo de regressão (`RandomForestRegressor`) para prever o salário com base na idade.  Este serviço é o coração do nosso sistema, como o cérebro que processa informações e toma decisões.  Ele recebe dados normalizados como entrada e treina o modelo periodicamente, salvando o modelo treinado em um arquivo `.joblib`.

4. **Consumidor de Previsões:**  Consome as previsões geradas pelo modelo treinado e as utiliza para outras aplicações.  Este serviço é o elo final da nossa cadeia, como o consumidor final que utiliza o produto.  Ele faz requisições periódicas à API do treinador para obter previsões de salário.


## Diagrama de Arquitetura

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

## Tecnologias

* **Python:** Linguagem de programação principal.
* **FastAPI:** Framework para criação de APIs RESTful.
* **Scikit-learn:** Biblioteca para machine learning.
* **Pandas:** Biblioteca para manipulação de dados.
* **Faker:** Biblioteca para geração de dados sintéticos.


## Considerações Finais

Esta arquitetura modular e distribuída permite escalabilidade, flexibilidade e manutenção simplificada.  A inspiração veio da complexidade e beleza de um ecossistema natural, onde diferentes organismos interagem de forma harmoniosa e eficiente.  A busca pela perfeição neste projeto é semelhante à busca pela perfeição na arte, onde cada detalhe contribui para o resultado final.
