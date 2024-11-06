# Treinador de Modelo - Documentação 06/11/2024

**Elias Andrade - Arquiteto de Soluções Replika AI Solutions - Maringá, PR**

Este documento descreve o componente `treinador_stream.py` do pipeline de predição de salário.  Este componente é o coração do nosso sistema, como o cérebro que processa informações e toma decisões.  Ele é responsável por treinar um modelo de regressão para prever o salário com base na idade.

## Funcionalidade

🧠 O treinador utiliza um `RandomForestRegressor` do scikit-learn para treinar um modelo de regressão.  Ele recebe dados normalizados como entrada e treina o modelo periodicamente, salvando o modelo treinado em um arquivo `.joblib`.  A inspiração veio da capacidade do cérebro humano de aprender e se adaptar a novas informações, como a capacidade de um mestre artesão de aprimorar suas habilidades ao longo do tempo.

## Código

```python
# ... (código do treinador_stream.py) ...
```

## Design

O treinador segue uma arquitetura modular e escalável, permitindo que o modelo seja treinado e atualizado continuamente.  Ele é um microsserviço independente, que pode ser escalado horizontalmente para atender a demandas crescentes.  A inspiração veio da elegância e simplicidade do design modular.

## Considerações

* O intervalo de treinamento é configurável via variável de ambiente `INTERVALO_TREINAMENTO`.
* O modelo treinado é salvo na pasta `modelos`.

## Referências

* [Scikit-learn](https://scikit-learn.org/stable/)
