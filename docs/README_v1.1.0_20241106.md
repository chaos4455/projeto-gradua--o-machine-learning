# Sistema de Processamento de Stream de Dados - v1.1.0 (06/11/2024)

**Elias Andrade - Arquiteto de Soluções Replika AI Solutions Maringá - PR**

Este repositório contém o código para um sistema de processamento de stream de dados em tempo real, demonstrando um pipeline completo desde a geração de dados sintéticos até o consumo de previsões de um modelo de Machine Learning.  O sistema é construído utilizando microserviços baseados em FastAPI, permitindo alta modularidade, escalabilidade e manutenibilidade.  Imagine-o como uma pequena fábrica de dados, processando e transformando informações continuamente, semelhante à linha de montagem de uma fábrica de automóveis, mas para dados!

## Visão Geral:

O sistema é composto por quatro componentes principais, cada um funcionando como um serviço independente e comunicando-se via requisições HTTP:

* **Gerador de Dados:**  Este componente, inspirado na ideia de um fluxo contínuo de dados como uma "torneira" sempre aberta, gera dados sintéticos em tempo real utilizando a biblioteca `Faker`.  Ele simula um cenário real onde dados são constantemente alimentados em um sistema.  A frequência de geração é configurável, permitindo simular diferentes taxas de entrada de dados.  Imagine-o como a fonte primária de matéria-prima para nossa fábrica de dados.  A configuração é feita via variáveis de ambiente, permitindo flexibilidade e controle externo.

* **Normalizador:**  Este componente atua como um inspetor de qualidade, recebendo os dados brutos do Gerador e aplicando uma transformação crucial para o bom funcionamento do modelo de Machine Learning: a normalização.  Utilizando o `StandardScaler` do scikit-learn, ele garante que os dados numéricos tenham média 0 e desvio padrão 1, prevenindo que recursos com valores maiores dominem o modelo e melhorando a performance do treinamento.  Este processo é análogo à preparação cuidadosa dos materiais antes de serem usados na linha de montagem.

* **Treinador:**  O coração do nosso sistema, este componente treina um modelo de regressão `RandomForestRegressor` utilizando os dados normalizados recebidos do Normalizador.  O `RandomForestRegressor`, conhecido por sua robustez e capacidade de lidar com dados não lineares, é treinado periodicamente, criando um modelo atualizado constantemente.  Os modelos treinados são salvos em disco utilizando a biblioteca `joblib`, permitindo a persistência e o carregamento rápido do modelo para predições.  Este processo é semelhante ao treinamento contínuo de um trabalhador em uma linha de montagem, aprimorando suas habilidades com a experiência.

* **Consumidor:**  Este componente simula um sistema que utiliza as previsões do modelo treinado.  Ele periodicamente solicita previsões ao Treinador, enviando uma idade aleatória como entrada e registrando os resultados.  Imagine-o como o cliente final, recebendo o produto acabado (a predição) da nossa fábrica de dados.  A frequência de consumo é configurável, permitindo simular diferentes taxas de utilização do modelo.

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
                                   Banco de Dados (SQLite - Potencial Futuro)
```

## Detalhes Técnicos:

* **Linguagem:** Python 3.7+
* **Framework:** FastAPI (para a criação de APIs RESTful, escolhido por sua velocidade e facilidade de uso)
* **Bibliotecas:** `faker`, `pandas`, `scikit-learn`, `joblib`, `requests`, `asyncio`, `pydantic`
* **Modelo de Machine Learning:** `RandomForestRegressor` (escolhido por sua robustez e performance)
* **Comunicação:** Requisições HTTP entre os componentes (simples, eficiente e amplamente utilizado)
* **Arquitetura:** Microserviços (permitindo escalabilidade e manutenibilidade)
* **Programação:** Assíncrona (utilizando `asyncio` para otimizar a performance)

## Como Executar:

1. **Requisitos:**  Certifique-se de ter o Python 3.7+ instalado em seu sistema.
2. **Instalação:** Clone este repositório e execute `pip install -r requirements.txt` para instalar as dependências.
3. **Execução:** Execute cada componente em um terminal separado, utilizando os comandos `uvicorn` fornecidos na documentação individual de cada componente.  Lembre-se de que cada componente precisa estar em execução para que o sistema funcione corretamente.  A ordem de execução não é crítica, mas é recomendado iniciar o Gerador primeiro.

## Documentação Detalhada:

A documentação completa para cada componente, incluindo detalhes técnicos, exemplos de uso e considerações, está disponível na pasta `docs/componentes`.  A arquitetura geral do sistema é descrita em `docs/arquitetura.md`.

## Considerações Futuras:

* **Escalabilidade:** Implementar um sistema de mensagens assíncronas, como o Kafka, para melhorar a escalabilidade e o desacoplamento entre os componentes.  Isso permitiria lidar com um volume muito maior de dados e tornar o sistema mais robusto.
* **Persistência de Dados:** Integrar um banco de dados, como o PostgreSQL ou o MySQL, para persistir os dados gerados, os dados normalizados e as previsões.  Isso permitiria analisar os dados históricos e monitorar a performance do sistema ao longo do tempo.
* **Monitoramento:** Implementar um sistema de monitoramento para acompanhar a performance de cada componente, incluindo métricas como tempo de resposta, taxa de sucesso e erros.  Isso permitiria identificar e resolver problemas rapidamente.
* **Integração Contínua/Entrega Contínua (CI/CD):** Automatizar o processo de build, teste e deploy do sistema, garantindo a qualidade e a confiabilidade do código.  Isso permitiria lançar novas versões do sistema com mais frequência e segurança.
* **Interface Gráfica:** Desenvolver uma interface gráfica para monitorar o sistema em tempo real e visualizar os dados gerados e as previsões.  Isso melhoraria a experiência do usuário e facilitaria a análise dos dados.
* **Modelos de Machine Learning Alternativos:** Explorar outros modelos de Machine Learning para melhorar a precisão das previsões.  Isso permitiria otimizar o sistema para diferentes cenários e requisitos.
* **Testes:** Implementar testes unitários e de integração para garantir a qualidade do código e prevenir erros.  Isso melhoraria a confiabilidade do sistema e reduziria o tempo de desenvolvimento.


## Referências:

* **FastAPI:** [https://fastapi.tiangolo.com/](https://fastapi.tiangolo.com/)
* **Scikit-learn:** [https://scikit-learn.org/stable/](https://scikit-learn.org/stable/)
* **Faker:** [https://faker.readthedocs.io/en/master/](https://faker.readthedocs.io/en/master/)
* **Joblib:** [https://joblib.readthedocs.io/en/latest/](https://joblib.readthedocs.io/en/latest/)
* **Requests:** [https://requests.readthedocs.io/en/latest/](https://requests.readthedocs.io/en/latest/)
* **Asyncio:** [https://docs.python.org/3/library/asyncio.html](https://docs.python.org/3/library/asyncio.html)


## Licença:

(A ser definida)


## Inspirações:

Este projeto foi inspirado em sistemas de processamento de dados em tempo real de grande escala, como aqueles utilizados por empresas como o Google e o Netflix.  A arquitetura modular e escalável permite lidar com grandes volumes de dados e garante a flexibilidade necessária para futuras expansões.  A escolha das tecnologias foi baseada em sua maturidade, performance e facilidade de uso.  O projeto demonstra a capacidade de criar sistemas complexos e robustos para aplicações de Machine Learning em tempo real, utilizando conceitos de microserviços, programação assíncrona e melhores práticas de desenvolvimento de software.  A modularidade do sistema permite fácil expansão e manutenção, tornando-o uma base sólida para projetos futuros.  A analogia com uma linha de montagem industrial ilustra a natureza sequencial e eficiente do pipeline de dados.  A escolha do `RandomForestRegressor` foi inspirada em sua capacidade de lidar com dados não lineares e sua robustez a outliers, tornando-o uma escolha adequada para este cenário.  A utilização de variáveis de ambiente para configuração permite flexibilidade e controle externo, facilitando a integração com diferentes ambientes.  O uso de logs detalhados facilita a depuração e o monitoramento do sistema.  A documentação completa e bem estruturada garante a fácil compreensão e manutenção do código.  O projeto é um exemplo prático de como construir um sistema de processamento de dados em tempo real eficiente, escalável e robusto.
