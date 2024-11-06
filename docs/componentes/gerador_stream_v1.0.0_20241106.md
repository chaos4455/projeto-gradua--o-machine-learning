# Gerador de Stream de Dados - v1.0.0 (06/11/2024)

**Elias Andrade - Arquiteto de Soluções Replika AI Solutions Maringá - PR**

Este componente é responsável pela geração contínua de dados sintéticos, simulando um fluxo de dados em tempo real.  Ele utiliza a biblioteca FastAPI para criar uma API RESTful, permitindo acesso aos dados gerados e monitoramento do status do gerador.

## Funcionalidades:

* **Geração de Dados Sintéticos:** Gera dados aleatórios, mas realistas, usando a biblioteca `Faker`.  Os dados incluem nome, idade, salário, cidade e cargo.
* **API RESTful:** Exporta os dados via endpoints `/dados` e `/status`.
* **Geração em Background:** A geração de dados ocorre em segundo plano, sem bloquear a API.
* **Configuração:** O tamanho do buffer e o intervalo de geração são configuráveis via variáveis de ambiente (`TAMANHO_BUFFER` e `INTERVALO_GERACAO`).
* **Logging:** Implementa logging detalhado para monitoramento e depuração.
* **Tratamento de Erros:** Inclui tratamento de exceções para garantir a robustez do sistema.

## Arquitetura:

O componente utiliza o padrão de projeto `Producer-Consumer`, onde um processo gera os dados e outro os disponibiliza via API.  A geração de dados é feita em background usando `asyncio.create_task`.

![Diagrama de Arquitetura](diagrama_arquitetura.png)


## Tecnologias Utilizadas:

* **Python:** Linguagem de programação principal.
* **FastAPI:** Framework para criação de APIs RESTful.
* **Faker:** Biblioteca para geração de dados sintéticos.
* **Pandas:** Biblioteca para manipulação de dados.
* **Asyncio:** Biblioteca para programação assíncrona.
* **Logging:** Para monitoramento e depuração.
* **uvicorn:** Servidor ASGI para executar a aplicação FastAPI.


## Exemplos de Uso:

**Endpoint `/dados`:** Retorna um JSON com os dados gerados no formato:

```json
[
  {
    "nome": "Nome Completo",
    "idade": 30,
    "salario": 5000.0,
    "cidade": "Cidade",
    "cargo": "Cargo",
    "timestamp": "2024-11-06T10:00:00",
    "geracao_id": "uuid"
  },
  // ... mais dados
]
```

**Endpoint `/status`:** Retorna um JSON com o status do gerador:

```json
{
  "status": "ativo",
  "ultima_geracao": "2024-11-06T10:00:00",
  "total_geracoes": 10,
  "registros_atuais": 1000
}
```

## Considerações:

* A performance pode ser otimizada com o uso de técnicas de processamento paralelo ou distribuído para a geração de dados.
* A escalabilidade pode ser melhorada com o uso de um banco de dados para armazenar os dados gerados.

## Referências:

* [Documentação FastAPI](https://fastapi.tiangolo.com/)
* [Documentação Faker](https://faker.readthedocs.io/en/master/)


## Inspirações:

Este componente foi inspirado na necessidade de simular dados em tempo real para testes de performance e desenvolvimento de sistemas de processamento de stream de dados.  A escolha da FastAPI se deve à sua velocidade e facilidade de uso.  A geração de dados sintéticos é uma técnica comum em desenvolvimento de software, inspirada em conceitos de *data augmentation* usados em Machine Learning.  A arquitetura lembra a estrutura de um pipeline de dados, como em um sistema de *data streaming* moderno.  A escolha do nome "Gerador de Stream" é uma referência direta à natureza do componente, que gera um fluxo contínuo de dados.
