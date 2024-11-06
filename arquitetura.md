# Arquitetura do Projeto de Machine Learning (v0.0.01 rev.0001)

Este documento descreve a arquitetura do projeto de Machine Learning, incluindo as tecnologias utilizadas e a organização do código.

## Tecnologias:

* **Linguagem de Programação:** Python 🐍
* **Bibliotecas:** Pandas 🐼, NumPy 🔢, TensorFlow 🧠, Keras 🤖, Scikit-learn 🔬
* **Framework Web:** FastAPI 🚀
* **Banco de Dados:** SQLite 🪨
* **Visualização:** Dash 📊
* **Front-end:** HTML, CSS, JavaScript 🌐
* **Formato de Dados:** JSON, YAML, MD 📄, TXT 📝


## Arquitetura:

O projeto será dividido em três camadas principais:

* **Front-end:** Responsável pela interface do usuário, utilizando HTML, CSS e JavaScript.  O front-end se comunicará com o back-end através de chamadas à API RESTful.

* **Back-end:** Responsável pela lógica de negócio, utilizando FastAPI e Python.  O back-end se comunicará com o banco de dados SQLite e com o modelo de Machine Learning.

* **Middleware:**  Uma camada intermediária que irá lidar com a comunicação entre o front-end e o back-end, e também com o processamento de dados.  Esta camada irá utilizar as bibliotecas Pandas e NumPy para o pré-processamento de dados e o TensorFlow/Keras para o treinamento e utilização do modelo de Machine Learning.


## Diagrama de Componentes:

```
                                    +-----------------+
                                    |     Front-end   |
                                    +--------+--------+
                                            |
                                            |  API Calls
                                            v
                                    +--------+--------+
                                    |    Middleware   |
                                    +--------+--------+
                                            |
                                            | Data Processing, Model Inference
                                            v
                                    +--------+--------+
                                    |     Back-end    |  (FastAPI, Python)
                                    +--------+--------+
                                            |
                                            | Database Access
                                            v
                                    +--------+--------+
                                    |    Database     | (SQLite)
                                    +-----------------+

```

## Princípios de Design:

O projeto será desenvolvido seguindo os princípios DDD (Domain-Driven Design), SOLID e DRY (Don't Repeat Yourself).


## Formato de Saída:

Os resultados serão gerados em diferentes formatos, incluindo PNG (para gráficos), JSON e YAML (para dados estruturados) e MD (para relatórios).
