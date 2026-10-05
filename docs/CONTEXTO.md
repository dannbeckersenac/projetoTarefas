# Tarefa Certa

Controle de tarefas por checklist para um escritório de quatro pessoas que atende pedidos internos:
comprar material, tirar um documento, formatar um computador. Hoje o pedido chega por mensagem,
cada um tem várias etapas, e a única forma de saber o que já foi feito é perguntar para quem está fazendo.

## As respostas do kickoff

- **O que faz:** quem pede abre uma tarefa e acompanha o checklist dela; quem executa vê a fila,
  lança cada etapa feita e a conclusão. A situação da tarefa muda sozinha conforme os itens entram.
- **Quem usa:** dois perfis. A solicitante, que usa no celular, e o executor, que usa no computador.
  Neste projeto, os dois usam a API pelo `/docs`. O front fica para depois.
- **MVP:**
  1. abrir uma tarefa;
  2. listar as tarefas, com filtro por situação e por solicitante;
  3. ver uma tarefa;
  4. lançar um item no checklist de uma tarefa, aplicando a regra;
  5. listar os itens de uma tarefa.

## Os perfis

- **Solicitante** (Júlia, auxiliar administrativa). Abre tarefa com título, descrição e prazo. Vê só
  as tarefas dela e o checklist de cada uma.
- **Executor** (Marcos). Vê a fila inteira, filtrada por situação. Lança os itens do checklist.

Não existe login. Os usuários ficam numa lista fixa em memória, e quem pede informa o próprio id na
requisição (`solicitante_id`). Qualquer um pode trocar esse número: isso é conhecido e fica assim.

## A regra do serviço

- A tarefa nova começa com situação `aberta` e `itens_feitos` igual a `0`.
- Cada item tem um tipo: `etapa` ou `conclusao`.
- Um item `etapa` soma 1 em `itens_feitos` e muda a situação para `em andamento`.
- Um item `conclusao` muda a situação para `concluida`, sem mexer no contador.
- Tarefa `concluida` recusa qualquer item novo.

A regra mora no serviço de item. O serviço não levanta `HTTPException`: quando recusa, devolve um
texto com o motivo, e a rota escolhe o status.

## Os dados

Todos os dados ficam em listas na memória, dentro dos repositórios. Os ids são gerados com
`len(lista) + 1`.

**Usuário** (lista fixa, criada no próprio repositório, sem rota de cadastro)

| Campo | Tipo | Regra |
|---|---|---|
| `id` | int | gerado |
| `nome` | str | |
| `tipo` | str | `solicitante` ou `executor` |

Usuários iniciais: `1, "Júlia", "solicitante"`, `2, "Marcos", "executor"`, `3, "Paulo", "solicitante"`.

**Tarefa**

| Campo | Tipo | Regra |
|---|---|---|
| `id` | int | gerado |
| `titulo` | str | de 3 a 100 caracteres |
| `descricao` | str | até 500 caracteres |
| `prazo` | date | formato `AAAA-MM-DD` |
| `situacao` | str | `aberta`, `em andamento` ou `concluida`. Definida pelo serviço, nunca pela requisição |
| `itens_feitos` | int | começa em 0. Definido pelo serviço, nunca pela requisição |
| `solicitante_id` | int | precisa existir na lista de usuários e ser do tipo `solicitante` |

**Item do checklist**

| Campo | Tipo | Regra |
|---|---|---|
| `id` | int | gerado |
| `tarefa_id` | int | vem do caminho da rota, não do corpo |
| `tipo` | str | `etapa` ou `conclusao` |
| `descricao` | str | de 3 a 200 caracteres |
| `data` | date | preenchida pelo serviço com o dia de hoje |

## O contrato da API

| Capacidade | Método e caminho | Sucesso | Erros |
|---|---|---|---|
| Abrir tarefa | `POST /tarefas` | 201, a tarefa criada | 422 campo inválido ou solicitante que não existe |
| Listar tarefas | `GET /tarefas?situacao=&solicitante_id=` | 200, lista, os dois filtros opcionais | |
| Ver uma tarefa | `GET /tarefas/{tarefa_id}` | 200, a tarefa | 404 tarefa não encontrada |
| Lançar item | `POST /tarefas/{tarefa_id}/itens` | 201, o item criado | 404 tarefa não encontrada, 409 tarefa já concluída, 422 campo inválido |
| Listar itens | `GET /tarefas/{tarefa_id}/itens` | 200, lista | 404 tarefa não encontrada |

Toda rota que recebe `tarefa_id` usa uma dependência `tarefa_existente` com `Depends`, que devolve a
tarefa ou levanta o 404.

## A estrutura

Nomes de pasta, arquivo, função e variável em português. A chamada vai sempre na mesma direção:
rota chama serviço, serviço chama repositório.

```
tarefa-certa/
├── CONTEXTO.md
├── AGENTS.md
├── .docs/
├── .gitignore               venv/ e __pycache__/
├── requirements.txt         fastapi[standard] e pytest
├── main.py                  cria o app e liga os routers com include_router
├── rotas/
│   ├── __init__.py
│   └── tarefas.py           APIRouter, as cinco rotas e a dependência tarefa_existente
├── servicos/
│   ├── __init__.py
│   ├── tarefa.py            criar e listar com filtros
│   └── item.py              lançar item com a regra, listar itens
├── repositorios/
│   ├── __init__.py
│   ├── usuario.py           a lista fixa, buscar_por_id
│   ├── tarefa.py            a lista, listar, buscar_por_id, salvar
│   └── item.py              a lista, listar_por_tarefa, salvar
├── esquemas/
│   ├── __init__.py
│   ├── tarefa.py            TarefaCriar e TarefaSaida
│   └── item.py              ItemCriar e ItemSaida
└── testes/
    ├── __init__.py
    ├── test_tarefas.py
    └── test_itens.py
```

O que pode aparecer em cada pasta:

- `rotas/`: `APIRouter`, `HTTPException`, `Depends`, status code e os esquemas. Nenhuma lista, nenhuma conta.
- `servicos/`: os repositórios, os esquemas, as contas e a regra. Nenhum `HTTPException` nem status code.
  Quando não encontra, devolve `None`.
- `repositorios/`: a lista em memória e as funções que leem e gravam nela. Nada de regra.
- `esquemas/`: classes Pydantic com `BaseModel` e `Field`. O esquema de entrada não tem `id`, `situacao`
  nem `itens_feitos`.

Os testes usam o `TestClient` do FastAPI e chamam a API pelas rotas. Antes de cada teste, as listas de
tarefas e de itens são esvaziadas, para um teste não depender do outro.

## A ordem das tarefas

Cada uma cabe numa tarefa pequena de Executor. Não pule a ordem.

1. Esqueleto: pastas, `__init__.py`, `main.py` vazio de rotas, `requirements.txt`, configuração do pytest.
2. Esquemas de tarefa e repositório de usuário com a lista fixa.
3. Abrir tarefa: repositório, serviço e rota `POST /tarefas`, com a situação inicial e a checagem do solicitante.
4. Listar tarefas com os dois filtros.
5. Ver uma tarefa, com a dependência `tarefa_existente` e o 404.
6. Esquemas de item e listar itens de uma tarefa.
7. Lançar item com a regra: etapa, conclusão e a recusa em tarefa concluída.

## Fora do escopo

Prioridade, anexo, comentário, alerta de prazo vencido, reabrir tarefa, aviso por mensagem, apagar e
editar tarefa, cadastro de usuário, login e senha, banco de dados, front-end, deploy e `async def`.
Se alguma tarefa parecer precisar de algo desta lista, pare e pergunte.
