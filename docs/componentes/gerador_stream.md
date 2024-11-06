# Gerador de Dados - Documentação 06/11/2024

**Elias Andrade - Arquiteto de Soluções Replika AI Solutions - Maringá, PR**

Este documento descreve o componente `gerador_stream.py` do pipeline de predição de salário.  Este componente é a base da nossa operação, como a semente que dá origem a uma grande árvore.  Ele é responsável por gerar dados sintéticos, simulando informações realistas de indivíduos.

## Funcionalidade

🏭 O gerador cria dados aleatórios, mas com uma estrutura que imita dados reais.  Ele utiliza a biblioteca `Faker` para gerar nomes, idades, salários, cidades e cargos.  A inspiração veio da capacidade da natureza de gerar formas complexas e variadas, como um fractal que se repete infinitamente.

## Código

```python
# ... (código do gerador_stream.py) ...
```

## Design

O gerador segue o princípio KISS (Keep It Simple, Stupid), priorizando a simplicidade e a facilidade de manutenção.  Ele é um microsserviço independente, que pode ser escalado horizontalmente para atender a demandas crescentes.  A inspiração veio da elegância e simplicidade do design minimalista.

## Considerações

* O tamanho do buffer de dados gerados é configurável via variável de ambiente `TAMANHO_BUFFER`.
* O intervalo de geração de dados é configurável via variável de ambiente `INTERVALO_GERACAO`.

## Referências

* [Faker](https://faker.readthedocs.io/en/master/)
