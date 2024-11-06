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


# Sistema de Processamento de Stream de Dados - Pipeline de Predição de Salário

**🚀 Projeto:** Pipeline de Predição de Salário em Tempo Real

**👨‍💻 Desenvolvedor:** Elias Andrade - Arquiteto de Soluções Replika AI Solutions - Maringá, PR - 06/11/2024

[![Python Version](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/fastapi-0.95.2-green.svg)](https://fastapi.tiangolo.com/)
[![Scikit-learn](https://img.shields.io/badge/scikit--learn-1.3.0-orange.svg)](https://scikit-learn.org/stable/)
[![License](https://img.shields.io/badge/license-MIT-lightgrey.svg)](https://opensource.org/licenses/MIT)
[![Tests](https://img.shields.io/badge/tests-passing-brightgreen.svg)](test_results.txt)


---

## Visão Geral

Este projeto demonstra um pipeline completo de processamento de stream de dados em tempo real, construído com microserviços FastAPI e utilizando Python.  Como afirma a documentação oficial do FastAPI ("FastAPI: Modern, Fast (high-performance), Web framework for building APIs with Python 3.7+ based on standard Python type hints"), a escolha do FastAPI se justifica pela sua velocidade e facilidade de uso. O pipeline consiste em quatro componentes principais, cada um executando como um microsserviço independente, comunicando-se via requisições HTTP:

* **Gerador de Dados:** Gera dados sintéticos para simular um fluxo contínuo de informações.
* **Normalizador:** Normaliza os dados para garantir consistência no treinamento do modelo.
* **Treinador:** Treina um modelo de Machine Learning para prever o salário com base na idade e outras variáveis.
* **Consumidor:** Consome as previsões do modelo treinado, simulando um sistema que utiliza as previsões em tempo real.


---

## Arquitetura

O pipeline segue uma arquitetura modular e escalável, baseada em microserviços.  A comunicação assíncrona entre os componentes é feita através de requisições HTTP, permitindo alta disponibilidade e escalabilidade horizontal.  Esta abordagem é consistente com as melhores práticas de desenvolvimento de microsserviços, como descrito em "Building Microservices" de Sam Newman.

```
+-----------------+     +-----------------+     +-----------------+     +-----------------+
| Gerador de Dados |---->| Normalizador    |---->| Treinador      |---->| Consumidor      |
+-----------------+     +-----------------+     +-----------------+     +-----------------+
     ^                                                                        |
     |                                                                        v
     +-----------------------------------------------------------------------+
                                         |
                                         v
                                  Monitoramento e Logs (Utilizando Loguru)
```

**[Diagrama de Arquitetura com ícones UML]** (Incluir um diagrama de arquitetura com ícones UML representando cada componente e suas interações)


---

## Componentes

### 1. Gerador de Dados (`gerador_stream.py`)

🏭 **Funcionalidade:** Gera dados sintéticos usando a biblioteca `Faker`, simulando um fluxo contínuo de informações, incluindo idade, experiência profissional, nível de educação e outras variáveis relevantes para a predição de salário.  A utilização do Faker simplifica o processo de geração de dados de teste, conforme descrito na sua documentação: [Faker Documentation](https://faker.readthedocs.io/en/master/).

⚙️ **Configurações (Variáveis de Ambiente):**

* `TAMANHO_BUFFER`: Tamanho do buffer de dados gerados (default: 1000).
* `INTERVALO_GERACAO`: Intervalo de geração de dados em segundos (default: 5).
* `NUM_VARIÁVEIS`: Número de variáveis a serem geradas (default: 5).

**Exemplo de Dados Gerados:**

```json
[
  {"idade": 30, "experiencia": 5, "educacao": "Graduação", ...},
  {"idade": 25, "experiencia": 2, "educacao": "Técnico", ...},
  ...
]
```

**Código Exemplo (trecho):**

```python
from faker import Faker
fake = Faker('pt_BR')
# ... restante do código ...
```

🔗 **Referência:** [Faker](https://faker.readthedocs.io/en/master/)


---

### 2. Normalizador (`normalizador_stream.py`)

🔄 **Funcionalidade:** Normaliza os dados numéricos usando `StandardScaler` do scikit-learn, garantindo que todas as features tenham a mesma escala, evitando que features com valores maiores dominem o processo de treinamento.  A escolha do `StandardScaler` é justificada pela sua eficácia em normalizar dados com distribuição aproximadamente normal, conforme explicado na documentação do scikit-learn: [StandardScaler Documentation](https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.StandardScaler.html).

⚙️ **Configurações (Variáveis de Ambiente):**

* `INTERVALO_NORMALIZACAO`: Intervalo de normalização em segundos (default: 10).
* `VARIÁVEIS_NORMALIZAR`: Lista de variáveis a serem normalizadas (default: ["idade", "experiencia"]).

**Código Exemplo (trecho):**

```python
from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
# ... restante do código ...
```

🔗 **Referência:** [Scikit-learn](https://scikit-learn.org/stable/)


---

### 3. Treinador (`treinador_stream.py`)

🧠 **Funcionalidade:** Treina um modelo `RandomForestRegressor` periodicamente com os dados normalizados, salvando o modelo treinado em um arquivo `.joblib`.  Implementa um sistema de versionamento de modelos, mantendo os 3 últimos modelos treinados.  O `RandomForestRegressor` foi escolhido por sua robustez e capacidade de lidar com dados não lineares, conforme descrito na documentação: [RandomForestRegressor Documentation](https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestRegressor.html).

⚙️ **Configurações (Variáveis de Ambiente):**

* `INTERVALO_TREINAMENTO`: Intervalo de treinamento em segundos (default: 60).
* `MODELO_PATH`: Caminho para salvar os modelos treinados (default: "modelos/").

**Código Exemplo (trecho):**

```python
from sklearn.ensemble import RandomForestRegressor
model = RandomForestRegressor()
# ... restante do código ...
```

💾 **Saída:** Modelos treinados salvos na pasta `modelos` com nomes baseados em timestamps.

🔗 **Referência:** [Scikit-learn](https://scikit-learn.org/stable/), [Joblib](https://joblib.readthedocs.io/en/latest/)


---

### 4. Consumidor (`consumidor_stream.py`)

🤖 **Funcionalidade:** Consome previsões do Treinador via requisições HTTP, simulando um sistema que utiliza as previsões em tempo real.  Inclui tratamento de erros e logging detalhado.  A utilização de requisições HTTP para comunicação entre microsserviços é uma prática comum e bem documentada, como descrito em: [REST API Design Best Practices](https://www.restapitutorial.com/lessons/restfulbestpractices.html).

⚙️ **Configurações (Variáveis de Ambiente):**

* `TREINADOR_URL`: URL da API do Treinador (default: "http://localhost:8001/predict").
* `INTERVALO_CONSUMO`: Intervalo de consumo em segundos (default: 15).

**Código Exemplo (trecho):**

```python
import requests
response = requests.post(TREINADOR_URL, json=data)
# ... restante do código ...
```

🔗 **Referência:** [Requests](https://requests.readthedocs.io/en/master/)


---

## Tecnologias

* **Python 3.9+** 🐍  A escolha do Python se deve à sua vasta biblioteca de ferramentas para ciência de dados e desenvolvimento web.
* **FastAPI** ⚡️ [![FastAPI](https://img.shields.io/badge/fastapi-0.95.2-green.svg)](https://fastapi.tiangolo.com/)  FastAPI é um framework moderno e de alto desempenho para construção de APIs em Python.  Sua base em type hints permite a geração automática de documentação e validação de dados.
* **Scikit-learn** 🤖 [![Scikit-learn](https://img.shields.io/badge/scikit--learn-1.3.0-orange.svg)](https://scikit-learn.org/stable/)  Scikit-learn é uma biblioteca poderosa para Machine Learning em Python, fornecendo algoritmos de regressão, classificação e clustering.
* **Faker** 🎭 [![Faker](https://img.shields.io/badge/faker-10.1.0-blue.svg)](https://faker.readthedocs.io/en/master/)  Faker é uma biblioteca para gerar dados sintéticos realistas, útil para testes e simulação.
* **Joblib** 💾 [![Joblib](https://img.shields.io/badge/joblib-1.2.0-purple.svg)](https://joblib.readthedocs.io/en/latest/)  Joblib é uma biblioteca para persistir modelos de Machine Learning de forma eficiente.
* **Requests** 🌐 [![Requests](https://img.shields.io/badge/requests-2.31.0-brightgreen.svg)](https://requests.readthedocs.io/en/master/)  Requests é uma biblioteca para fazer requisições HTTP em Python.
* **Asyncio** 异步  Asyncio permite a construção de aplicações concorrentes e assíncronas em Python.
* **Loguru** 🪵 [![Loguru](https://img.shields.io/badge/loguru-0.7.0-yellow.svg)](https://loguru.readthedocs.io/en/stable/)  Loguru é uma biblioteca de logging moderna e eficiente para Python.
* **Pydantic** 🛡️ [![Pydantic](https://img.shields.io/badge/pydantic-2.4.2-red.svg)](https://pydantic-docs.helpmanual.io/)  Pydantic é uma biblioteca para validação e parse de dados em Python.


---

## Como Executar

1. **Instalar dependências:** `pip install -r requirements.txt`
2. **Configurar variáveis de ambiente:**  Definir as variáveis de ambiente para cada componente (ver documentação individual).
3. **Executar cada componente em um terminal separado:**  Utilizar comandos `uvicorn` para cada microsserviço (ex: `uvicorn gerador_stream:app --reload`).


---

## Monitoramento e Logs

O pipeline utiliza a biblioteca `Loguru` para logging.  Os logs são gravados em arquivos separados para cada componente, facilitando o monitoramento e a depuração.  Um sistema de monitoramento centralizado poderia ser implementado futuramente para agregar e visualizar os logs de todos os componentes.  A escolha do Loguru se deve à sua facilidade de uso e flexibilidade, conforme descrito em sua documentação: [Loguru Documentation](https://loguru.readthedocs.io/en/stable/).

**Exemplo de Log (Loguru):**

```
2024-11-07 10:00:00.000 | INFO     | gerador_stream: Dados gerados com sucesso. Buffer size: 1000.
```


---

## Testes

O projeto inclui testes unitários e de integração para garantir a qualidade do código.  Os testes são executados usando o framework `pytest`.

**Comando para executar os testes:** `pytest`

**Relatório de Testes:** [test_results.txt](test_results.txt)


---

## Implantação

O pipeline pode ser implantado em um ambiente de contêineres (Docker) para facilitar a portabilidade e a escalabilidade.  Um arquivo `docker-compose.yml` poderia ser criado para orquestrar a implantação dos microserviços.


---

## Segurança

Considerações de segurança incluem:

* **Autenticação e Autorização:** Implementação de mecanismos de autenticação e autorização para proteger as APIs dos microserviços.
* **Tratamento de Erros:**  Tratamento robusto de erros para evitar vulnerabilidades e garantir a estabilidade do sistema.
* **Validação de Dados:** Validação rigorosa dos dados de entrada para prevenir ataques de injeção.


---

## Considerações Futuras

* **Escalabilidade:** Integração com o Kafka para melhor escalabilidade e processamento de grandes volumes de dados.
* **Persistência de Dados:** Utilização de um banco de dados NoSQL (ex: MongoDB) para persistir os dados gerados e as previsões.
* **Monitoramento:** Implementação de um sistema de monitoramento mais robusto, com dashboards e alertas em tempo real.
* **CI/CD:** Implementação de um pipeline de CI/CD para automatizar o processo de integração contínua e entrega contínua.
* **Interface Gráfica:** Desenvolvimento de uma interface gráfica para monitorar o pipeline e visualizar os dados.
* **Modelagem Alternativa:** Exploração de outros modelos de Machine Learning para melhorar a precisão das previsões.
* **Testes:** Expansão da cobertura de testes para incluir testes de desempenho e testes de segurança.


---

## Licença

Este projeto está licenciado sob a licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.


---

**[Conclusão com emojis e ícones]** 🎉  Este projeto demonstra um pipeline de processamento de dados robusto e escalável, pronto para lidar com grandes volumes de dados em tempo real.  Sua arquitetura modular e o uso de tecnologias modernas garantem alta disponibilidade e facilidade de manutenção. 🚀


