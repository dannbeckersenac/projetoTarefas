# 002 — Alinhar a conexão SQLAlchemy com MySQL
Agente: Executor Pesado — corrige a integração entre configuração, driver e fábrica de sessões em três arquivos.
Objetivo: deixar `banco.py` importável e conectar ao schema já criado `tarefa_certa`, preparando a base ORM para os modelos.

## Arquivos que PODE editar
- `backend/requirements.txt` → declarar SQLAlchemy e o driver que a URL existente usa.
- `backend/configuracao.py` → converter a porta do `.env` para inteiro ao criar a URL SQLAlchemy.
- `backend/banco.py` → consumir a URL existente, preservar `engine`, `Sessao` e `Base`, e disponibilizar a sessão para as rotas futuras.

## Contrato (não pode mudar)
- A URL usa o driver `mysql+mysqlconnector` e os valores já presentes no `.env`: `BANCO_USUARIO`, `BANCO_SENHA`, `BANCO_HOST`, `BANCO_PORTA` e `BANCO_NOME`.
- `configuracao.url_do_banco` é um objeto `sqlalchemy.engine.URL` criado por `URL.create`; `BANCO_PORTA` é convertida para `int`.
- `banco.engine` é criado com `create_engine(configuracao.url_do_banco)`.
- `banco.Sessao` é `sessionmaker(bind=engine)`.
- `banco.Base` continua sendo uma classe que herda de `DeclarativeBase`.
- `banco.obter_sessao()` cria e fornece uma sessão; ao terminar o uso, fecha a sessão.
- Dependências novas exatas: `SQLAlchemy` e `mysql-connector-python`.
- O schema alvo existente é `tarefa_certa`; não criar nem apagar schemas ou tabelas nesta tarefa.

## Passo a passo
1. Acrescentar `SQLAlchemy` e `mysql-connector-python` a `backend/requirements.txt`, sem remover as dependências atuais.
2. Converter `BANCO_PORTA` para inteiro em `configuracao.py`, preservando as cinco chaves atuais e `ORIGEM_FRONTEND`.
3. Corrigir `banco.py` para importar `url_do_banco` diretamente de `configuracao.py`; não chamar `obter_configuracao`, pois essa função não existe.
4. Manter `engine`, `Sessao` e `Base` e acrescentar `obter_sessao()` com fechamento da sessão ao terminar.
5. Antes da delegação, o responsável pelo projeto cria `backend/testes/test_banco.py` com um cenário de conexão ao schema e outro de encerramento da sessão; o executor não edita testes.
6. Instalar as dependências declaradas no venv e rodar o teste da tarefa, a suíte e a verificação sintática.

## Exemplos
- `.env` configura `BANCO_NOME=tarefa_certa` e porta `3306` → `engine.url.database` é `tarefa_certa` e a porta da URL é o inteiro `3306`.
- conexão com credenciais válidas → consulta `SELECT 1` retorna `1`.
- caso de erro: credenciais inválidas → teste de conexão falha; o código não tenta criar usuário nem schema.

## Pronto quando
- O comando `pytest testes/test_banco.py` passar.
- O comando `pytest` passar.
- O comando `python -m compileall -q .` passar.
- O comando `python -c "from banco import engine; print(engine.url.database)"` imprimir `tarefa_certa`.

## Cenários de validação (para o Tester)
| # | Ação (comando exato) | Resultado esperado |
|---|---|---|
| 1 | na pasta `backend`, executar `python -c "from banco import engine; print(engine.url.database)"` | saída contém `tarefa_certa`, sem imprimir usuário ou senha |
| 2 | na pasta `backend`, executar `python -c "from banco import engine; conexao = engine.connect(); resultado = conexao.exec_driver_sql('SELECT 1').scalar(); conexao.close(); print(resultado)"` | saída `1` |

## Proibido nesta task
- Criar classes/tabelas ORM, `criar_tabelas.py`, ou regras de negócio; esses itens terão plano próprio.
- Alterar rotas, serviços, repositórios, esquemas ou frontend.
- Ler ou exibir valores do `.env` nos logs ou na resposta.
- Mudar o nome do schema, usuário, host ou driver configurado no `.env`.
- Instalar dependências além de `SQLAlchemy` e `mysql-connector-python`.

## Dicas
- No estado atual, `banco.py` importa `obter_configuracao`, mas essa função não está definida em `configuracao.py`; use `configuracao.url_do_banco`, que já existe.
- A instalação atual do venv não contém SQLAlchemy nem `mysql-connector-python`, e `requirements.txt` ainda não os declara.
- Depois desta tarefa, criar um plano separado para as classes `Usuario`, `Tarefa` e `Item` em `modelos/`.

