# Normalizador de Dados - Documentação 06/11/2024

**Elias Andrade - Arquiteto de Soluções Replika AI Solutions - Maringá, PR**

Este documento descreve o componente `normalizador_stream.py` do pipeline de predição de salário.  Este componente é crucial para o sucesso do nosso modelo, como a base sólida de uma construção.  Ele é responsável por normalizar os dados gerados, preparando-os para o treinamento do modelo de machine learning.

## Funcionalidade

🔄 O normalizador utiliza o `StandardScaler` do scikit-learn para normalizar as colunas 'idade' e 'salario'.  Isso garante que todas as features tenham a mesma escala, evitando que features com valores maiores dominem o processo de treinamento.  A inspiração veio da busca pela harmonia e equilíbrio, como a busca pela perfeição na arte.

## Código

```python
# ... (código do normalizador_stream.py) ...
```

## Design

O normalizador segue uma arquitetura simples e eficiente, utilizando uma abordagem de pipeline para processar os dados.  Ele é um microsserviço independente, que pode ser escalado horizontalmente para atender a demandas crescentes.  A inspiração veio da elegância e simplicidade do design minimalista.

## Considerações

* O intervalo de normalização é configurável via variável de ambiente `INTERVALO_NORMALIZACAO`.

## Referências

* [Scikit-learn](https://scikit-learn.org/stable/)
