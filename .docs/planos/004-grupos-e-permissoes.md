# 004 — Grupos de usuários e permissões por rota

Agente: Executor.

## Objetivo

Trocar a coluna `usuarios.tipo` por **grupos com permissões guardados no banco** (RBAC). As duas personas viram dois grupos, `solicitante` e `executor`. Cada grupo tem uma lista de permissões, e cada rota protegida pede uma permissão. Um usuário que tem login mas cujo grupo não tem a permissão recebe 403. Além disso, quem não tem a permissão `tarefas:ver_todas` (a solicitante) só vê as próprias tarefas.

**Assunto novo:** todo trecho criado ou alterado por este plano leva um comentário que começa com `# Aula 10 · grupos:` e explica o que o trecho faz. No JSX, o marcador é `{/* Aula 10 · grupos: ... */}`. Não remover os comentários das aulas anteriores. Quando um trecho antigo sair, deixar um comentário curto mostrando como era, no mesmo estilo de `repositorios/usuario.py` ("Antes: ...").

## Arquivos que PODE editar

- `backend/modelos/grupo.py` (novo) → modelos `Grupo`, `Permissao` e a tabela de ligação `grupo_permissoes`.
- `backend/modelos/usuario.py` → trocar `tipo` por `grupo_id` (FK) e o relationship `grupo`.
- `backend/migracoes/versions/<revisao>_criado_grupos_e_permissoes.py` (novo, gerado pelo comando do passo 2) → tabelas, dados iniciais e migração dos usuários.
- `backend/migracoes/env.py` → importar o módulo `grupo` junto dos outros modelos.
- `backend/criar_tabelas.py` → importar os modelos novos e atualizar o comentário do INSERT.
- `backend/repositorios/grupo.py` (novo) → `buscar_por_nome`.
- `backend/esquemas/usuario.py` → `GrupoSaida`; `grupo` no lugar de `tipo` na entrada e na saída.
- `backend/servicos/usuario.py` → cadastro com grupo e `tem_permissao`.
- `backend/servicos/tarefa.py` → tirar a checagem de `tipo`; filtrar por dono em `listar` e na busca.
- `backend/rotas/autenticacao.py` → dependência `exigir_permissao`.
- `backend/rotas/tarefas.py`, `backend/rotas/itens.py`, `backend/rotas/usuarios.py` → trocar `obter_usuario_atual` por `exigir_permissao(...)` conforme a matriz.
- `frontend/src/App.jsx` → ler `usuario.grupo.nome` no lugar de `usuario.tipo`.

Não editar outros arquivos.

## Contrato (não pode mudar)

### Banco

| Tabela | Colunas |
|---|---|
| `grupos` | `id` INT PK, `nome` VARCHAR(20) NOT NULL UNIQUE (`uq_grupo_nome`) |
| `permissoes` | `id` INT PK, `nome` VARCHAR(50) NOT NULL UNIQUE (`uq_permissao_nome`), `descricao` VARCHAR(200) NOT NULL |
| `grupo_permissoes` | `grupo_id` FK `grupos.id` (`fk_grupo_permissoes_grupo`), `permissao_id` FK `permissoes.id` (`fk_grupo_permissoes_permissao`); PK composta pelas duas |
| `usuarios` | sai `tipo`; entra `grupo_id` INT NOT NULL, FK `grupos.id` (`fk_usuario_grupo`) |

Dados iniciais (criados pela migration, com estes ids):

- Grupos: `1 solicitante`, `2 executor`.
- Permissões e quem recebe:

| Permissão | Descrição | solicitante | executor |
|---|---|:---:|:---:|
| `tarefas:criar` | Abrir tarefa | ✔ | |
| `tarefas:listar` | Listar tarefas | ✔ | ✔ |
| `tarefas:ver` | Ver uma tarefa | ✔ | ✔ |
| `tarefas:ver_todas` | Ver tarefas de qualquer solicitante | | ✔ |
| `itens:lancar` | Lançar item no checklist | | ✔ |
| `itens:listar` | Listar itens de uma tarefa | ✔ | ✔ |
| `usuarios:listar` | Listar usuários | | ✔ |
| `usuarios:ver` | Ver um usuário pelo id | | ✔ |

### Rotas

| Rota | Proteção |
|---|---|
| `POST /usuarios` | aberta (sem mudança) |
| `POST /login` | aberta (sem mudança) |
| `GET /usuarios/eu` | só login (`obter_usuario_atual`), os dois grupos |
| `POST /tarefas` | `tarefas:criar` |
| `GET /tarefas` | `tarefas:listar` |
| `GET /tarefas/{tarefa_id}` | `tarefas:ver` |
| `POST /tarefas/{tarefa_id}/itens` | `itens:lancar` |
| `GET /tarefas/{tarefa_id}/itens` | `itens:listar` |
| `GET /usuarios` | `usuarios:listar` |
| `GET /usuarios/{usuario_id}` | `usuarios:ver` |

- Sem token ou com token inválido: 401, como hoje. Login válido sem a permissão: **403**, detalhe `Seu grupo não tem permissão para esta ação`.
- A checagem de permissão vem **antes** da busca da tarefa: na assinatura da rota, o `Depends(exigir_permissao(...))` é o primeiro parâmetro de dependência, antes de `tarefa=Depends(tarefa_existente)`. Assim, o 403 aparece antes do 404.
- **Dono da tarefa:** quem não tem `tarefas:ver_todas`:
  - em `GET /tarefas`, recebe só as tarefas com `solicitante_id` igual ao próprio id. O parâmetro `solicitante_id` da URL é ignorado.
  - em qualquer rota com `tarefa_id` de uma tarefa de outra pessoa, recebe **404** `Tarefa não encontrada`, igual a uma tarefa que não existe. Assim ninguém descobre quais ids existem.
- **Mudança de contrato aceita:** `POST /tarefas` feito por executor passa de 422 para 403.
- Cadastro: a entrada troca `tipo` por `grupo: str = Field(default="solicitante", pattern="^(solicitante|executor)$")`. A saída troca `tipo` por `grupo: GrupoSaida` (`{"id": int, "nome": str}`). Senha e hash continuam fora da resposta.

### Código

- `rotas/autenticacao.py`: `exigir_permissao(permissao: str)` devolve uma função de dependência. Essa função pede `usuario=Depends(obter_usuario_atual)`, levanta 403 quando `servico_usuario.tem_permissao(usuario, permissao)` é falso e devolve o usuário.
- `servicos/usuario.py`: `tem_permissao(usuario, permissao: str) -> bool` lê `usuario.grupo.permissoes` e compara o `nome`. Sem HTTPException.
- `servicos/tarefa.py`:
  - `criar(sessao, dados, usuario)` perde a checagem de `tipo` (a rota já garantiu a permissão) e não devolve mais texto.
  - `listar(sessao, situacao, solicitante_id, pagina, usuario)` troca o `solicitante_id` por `usuario.id` quando falta `tarefas:ver_todas`.
  - `buscar_por_id(sessao, tarefa_id, usuario)` devolve `None` quando a tarefa não existe **ou** é de outra pessoa e falta `tarefas:ver_todas`.
- `repositorios/grupo.py`: `buscar_por_nome(sessao, nome: str)` devolve o `Grupo` ou `None`.
- Fluxo rota → serviço → repositório mantido. O serviço não importa modelo.

## Passo a passo

1. **Modelos.** Criar `modelos/grupo.py`:
   - `grupo_permissoes = Table(...)` com as duas FKs nomeadas e a PK composta;
   - `Permissao`;
   - `Grupo`, com `permissoes = relationship("Permissao", secondary=grupo_permissoes)`.

   Em `modelos/usuario.py`, tirar `tipo`, criar `grupo_id` com `ForeignKey("grupos.id", name="fk_usuario_grupo")` e `grupo = relationship("Grupo")`, e importar `Grupo` como os outros modelos fazem. Incluir `grupo` no import de `migracoes/env.py` e os modelos novos em `criar_tabelas.py`.
2. **Migration.** Na pasta `backend`, rodar `.\venv\Scripts\alembic.exe revision -m "criado grupos e permissoes"`. O comando cria o arquivo com `down_revision = '51b1e88d2cc1'`. Conferir isso antes de seguir. Escrever o corpo à mão, no estilo de `51b1e88d2cc1_...py`:
   - `upgrade`:
     1. criar as três tabelas;
     2. `op.bulk_insert` dos grupos, das permissões e das ligações da matriz;
     3. `add_column` de `grupo_id` aceitando NULL (a tabela já tem linhas);
     4. `UPDATE usuarios SET grupo_id = 1 WHERE tipo = 'solicitante'` e `grupo_id = 2 WHERE tipo = 'executor'`;
     5. `alter_column` para NOT NULL;
     6. `create_foreign_key('fk_usuario_grupo', ...)`;
     7. `drop_column('usuarios', 'tipo')`.
   - `downgrade`: o caminho inverso. Recriar `tipo` aceitando NULL, preencher pelo `grupo_id`, passar para NOT NULL, remover a FK e a coluna `grupo_id`, e por fim apagar as três tabelas na ordem `grupo_permissoes`, `permissoes`, `grupos`.
   - **Não rodar** `alembic upgrade`. Quem aplica no banco é o usuário (ver Verificação manual).
3. **Repositório e esquemas.** Criar `repositorios/grupo.py` com `buscar_por_nome`. Em `esquemas/usuario.py`, criar `GrupoSaida` e trocar `tipo` por `grupo` em `UsuarioCriar` e `UsuarioSaida`.
4. **Serviço de usuário.** No `criar`, buscar o grupo pelo nome e gravar `grupo_id`. Se o grupo não existir no banco, devolver o texto `Grupo não cadastrado`. Criar `tem_permissao`.
5. **Dependência.** Criar `exigir_permissao` em `rotas/autenticacao.py`, logo abaixo de `obter_usuario_atual`.
6. **Rotas e serviço de tarefa.**
   - Aplicar a matriz em `rotas/tarefas.py`, `rotas/itens.py` e `rotas/usuarios.py`, com a dependência de permissão como primeiro parâmetro de dependência.
   - `tarefa_existente` passa o `usuario` para `servico.buscar_por_id`.
   - `criar_tarefa` perde o ramo do 422.
   - `listar_tarefas` passa o `usuario` ao serviço.
   - Ajustar `servicos/tarefa.py` conforme o contrato.
7. **Front.** Em `App.jsx`, trocar as três leituras de `usuario.tipo` por `usuario.grupo.nome`.
8. **Revisão.** `python -m compileall -q .` na pasta `backend`. Conferir que só os arquivos listados mudaram e que todo trecho novo tem o marcador `Aula 10 · grupos:`.

## Exemplos

- Júlia (solicitante) faz `POST /tarefas` → 201.
- Marcos (executor) faz `POST /tarefas` → 403 `Seu grupo não tem permissão para esta ação`.
- Júlia faz `POST /tarefas/1/itens` → 403, mesmo que a tarefa 1 seja dela.
- Júlia faz `GET /tarefas?solicitante_id=3` → só as tarefas dela.
- Júlia faz `GET /tarefas/{id de uma tarefa do Paulo}` → 404.
- Marcos faz `GET /tarefas` → todas as tarefas; `GET /usuarios` → 200.
- Júlia faz `GET /usuarios` → 403; `GET /usuarios/eu` → 200, com `"grupo": {"id": 1, "nome": "solicitante"}`.
- Sem token, qualquer rota protegida → 401.

## Pronto quando

- As três tabelas e a coluna `usuarios.grupo_id` existem pela migration, e `usuarios.tipo` não existe mais.
- Todas as linhas da tabela de rotas respondem como o contrato diz.
- `python -m compileall -q .` não acusa erro.
- Nenhum arquivo fora da lista foi editado, e todo código novo está comentado com o marcador.

## Verificação manual sugerida

1. Na pasta `backend`, rodar `.\venv\Scripts\alembic.exe upgrade head`. No MySQL, conferir com `SELECT * FROM grupos;`, `SELECT * FROM grupo_permissoes;` e `SHOW CREATE TABLE usuarios;` (deve aparecer `fk_usuario_grupo`).
2. Subir a API e, no `/docs`, fazer login como uma solicitante e como um executor. Testar cada linha da tabela de exemplos.
3. Opcional: rodar `alembic downgrade -1` e depois `alembic upgrade head` para conferir que a migration sabe voltar.

## Riscos conhecidos (fora do escopo, ficam para outro plano)

- `POST /usuarios` é aberto e aceita `grupo: "executor"`. Qualquer pessoa consegue se cadastrar como executor. Isso já acontece hoje com `tipo`, e esta tarefa não muda esse comportamento.
- Não haverá rotas para criar grupos ou mudar permissões. A matriz muda por migration.
- `backend/testes/` está vazio. Os testes automáticos destas regras ficam para um plano próprio.

## Proibido nesta tarefa

- Alterar `seguranca.py`, `.env`, `configuracao.py`, `banco.py` ou migrations já existentes.
- Rodar `alembic upgrade` ou `downgrade`, ou apagar dados do banco.
- Instalar dependências ou criar arquivos que não estão na lista.
- Guardar a matriz de permissões no código Python. Ela mora só no banco.
