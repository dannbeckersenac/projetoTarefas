# Arquitetura

A interface React conversa por HTTP com a API FastAPI usando `fetch`.

## Estado atual

O usuário criou o schema MySQL `tarefa_certa`, adicionou `backend/.env`, `backend/configuracao.py` e `backend/banco.py`, e escolheu a URL SQLAlchemy com o driver `mysql+mysqlconnector`. As classes ORM ainda não foram criadas. A configuração da conexão precisa de um ajuste aprovado antes de criar e importar os modelos.

## Camadas do backend

O fluxo permanece **rota → serviço → repositório**. A rota valida a chamada e escolhe o status HTTP; o serviço aplica as regras da cartilha; o repositório lê e grava os dados usando a sessão SQLAlchemy. Esquemas Pydantic continuam definindo entrada e saída da API. Os modelos ORM representam as tabelas `usuarios`, `tarefas` e `itens`.

Dependências do banco previstas: `SQLAlchemy` e `mysql-connector-python`. A instalação e a configuração de conexão estão descritas no plano 002 e aguardam aprovação.
