# Pipeline de Predição de Salário - Documentação 06/11/2024 - v1.1

**Elias Andrade - Arquiteto de Soluções Replika AI Solutions - Maringá, PR**

Este documento descreve o pipeline de predição de salário, um sistema de processamento de dados em tempo real que utiliza machine learning para prever o salário de um indivíduo com base em sua idade.  Este projeto é uma jornada rumo à inovação, como a busca pela pedra filosofal dos alquimistas.  Assim como os alquimistas buscavam a transmutação de metais, nós buscamos a transmutação de dados em conhecimento.

## Visão Geral 

🚀 Este pipeline utiliza uma arquitetura de microsserviços, inspirada na elegância e eficiência da natureza, como a intrincada rede de um formigueiro.  Cada componente opera de forma independente, permitindo escalabilidade e flexibilidade.  A modularidade permite que cada parte seja atualizada e melhorada sem afetar o funcionamento do sistema como um todo.

![Arquitetura do Pipeline](arquitetura.png)  **(Diagrama a ser adicionado)**

## Componentes Principais

* **Gerador de Dados (`gerador_stream.py`):** 🏭 Gera dados sintéticos, simulando informações realistas de indivíduos.  A inspiração veio da capacidade de criação e inovação da natureza, que constantemente gera novas formas de vida.  Este componente é configurável através das variáveis de ambiente `TAMANHO_BUFFER` e `INTERVALO_GERACAO`.

* **Normalizador de Dados (`normalizador_stream.py`):** 🔄 Normaliza os dados usando `StandardScaler` para melhorar a performance do modelo de machine learning.  A inspiração veio da busca pela harmonia e equilíbrio, como a busca pela perfeição na arte.  Este componente é configurável através da variável de ambiente `INTERVALO_NORMALIZACAO`.

* **Treinador de Modelo (`treinador_stream.py`):** 🧠 Treina um modelo de regressão (`RandomForestRegressor`) para prever o salário com base na idade.  A inspiração veio da capacidade do cérebro humano de aprender e se adaptar a novas informações, como a capacidade de um mestre artesão de aprimorar suas habilidades ao longo do tempo.  Este componente é configurável através da variável de ambiente `INTERVALO_TREINAMENTO`.  Os modelos treinados são salvos na pasta `modelos`.

* **Consumidor de Previsões (`consumidor_stream.py`):** 🤖 Consome as previsões do modelo treinado e as utiliza para outras aplicações.  A inspiração veio da capacidade das máquinas de executar tarefas repetitivas com precisão e eficiência, como uma linha de montagem que produz produtos em série.  Este componente faz requisições a cada 60 segundos à API do treinador.

* **Lançador do Pipeline (`stream_pipeline_launcher.py`):** 🕹️ Inicia e monitora todos os serviços do pipeline, garantindo a execução contínua.  A inspiração veio da capacidade de orquestração e controle de um maestro em uma orquestra.  Este componente utiliza logs detalhados para monitoramento e tratamento de erros.


## Tecnologias Utilizadas

* **Python:** Linguagem de programação principal, escolhida por sua versatilidade e ampla comunidade.  🐍
* **FastAPI:** Framework para criação de APIs RESTful, conhecido por sua velocidade e facilidade de uso. 🚀
* **Scikit-learn:** Biblioteca para machine learning, oferecendo algoritmos robustos e eficientes. 🤖
* **Pandas:** Biblioteca para manipulação de dados, facilitando o processamento e análise de dados. 🐼
* **Faker:** Biblioteca para geração de dados sintéticos, permitindo a simulação de dados realistas. 🎭


## Próximos Passos

* Adicionar métricas de performance ao modelo, como RMSE, R², e MAE. 📊
* Implementar testes unitários e de integração para garantir a qualidade do código. 🧪
* Criar uma interface gráfica para monitorar o pipeline em tempo real. 🖥️
* Explorar outras técnicas de machine learning, como redes neurais, para melhorar a precisão do modelo. 🧠
* Implementar um sistema de versionamento mais robusto para os modelos treinados. 💾


## Referências

* [Scikit-learn](https://scikit-learn.org/stable/)
* [FastAPI](https://fastapi.tiangolo.com/)
* [Pandas](https://pandas.pydata.org/)
* [Faker](https://faker.readthedocs.io/en/master/)
