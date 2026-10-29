# Rotas de tarefas. Aqui só entra HTTP: status, HTTPException e esquemas.
# Aula 6 (slides 37 e 38): toda rota que chega ao banco pede a sessão com
# sessao=Depends(obter_sessao) e passa adiante: rota, serviço, repositório.
# O FastAPI abre a sessão quando a requisição chega e fecha quando a resposta sai.
from fastapi import APIRouter, Depends, HTTPException, Query

from banco import obter_sessao
from esquemas.tarefa import TarefaCriar, TarefaSaida
from rotas.autenticacao import exigir_permissao, obter_usuario_atual   # Aula 10 · grupos: + exigir_permissao
from servicos import tarefa as servico

router = APIRouter(prefix="/tarefas", tags=["tarefas"])


# Dependência da aula 4: toda rota com tarefa_id passa por aqui.
# Aula 6: ela também pede a sessão. Na mesma requisição, o FastAPI entrega a MESMA
# sessão para a dependência e para a rota. Por isso, quando a regra muda a tarefa,
# o commit do item sabe o que mudou.
# Aula 9: ela também pede o token. Assim, sem login, a resposta é 401 antes do 404,
# e quem não fez login não descobre quais tarefas existem.
# Aula 10 · grupos: ela passa o usuário ao serviço. Tarefa de outra pessoa, para quem
# não tem "tarefas:ver_todas", volta None e vira o MESMO 404 de tarefa que não existe.
# Assim a solicitante não descobre quais ids são de outras pessoas.
# A permissão da rota (tarefas:ver, itens:listar...) é conferida na própria rota, que
# pede o exigir_permissao ANTES desta dependência: o 403 sai antes do 404.
def tarefa_existente(tarefa_id: int, usuario=Depends(obter_usuario_atual),
                     sessao=Depends(obter_sessao)):
    tarefa = servico.buscar_por_id(sessao, tarefa_id, usuario)
    if tarefa is None:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    return tarefa


# Abre uma tarefa. 201 com a tarefa criada, já com o id que o banco gerou.
# Aula 9: toda rota da cartilha pede o token com usuario=Depends(obter_usuario_atual).
# Aula 10 · grupos: agora pede a permissão "tarefas:criar", que só o grupo solicitante tem.
# Executor recebe 403 aqui na porta. Antes, o serviço conferia o tipo e a rota devolvia 422:
#     if isinstance(resultado, str):
#         raise HTTPException(status_code=422, detail=resultado)
@router.post("", response_model=TarefaSaida, status_code=201)
def criar_tarefa(dados: TarefaCriar, usuario=Depends(exigir_permissao("tarefas:criar")),
                 sessao=Depends(obter_sessao)):
    return servico.criar(sessao, dados, usuario)


# Lista as tarefas, com os filtros opcionais e a página.
# Query(default=1, ge=1): sem página na URL, vale 1; o ge (maior ou igual) é o mesmo
# do Field, então pagina=0 volta 422 antes de chegar ao serviço.
# Aula 10 · grupos: pede "tarefas:listar" e passa o usuário ao serviço, que decide
# se ele vê a fila inteira ou só as tarefas dele.
@router.get("", response_model=list[TarefaSaida])
def listar_tarefas(
    situacao: str | None = None,
    solicitante_id: int | None = None,
    pagina: int = Query(default=1, ge=1),
    usuario=Depends(exigir_permissao("tarefas:listar")),
    sessao=Depends(obter_sessao),
):
    return servico.listar(sessao, situacao, solicitante_id, pagina, usuario)


# Mostra uma tarefa. O Depends já resolveu o 404 antes de chegar aqui.
# Aula 10 · grupos: a permissão vem primeiro na assinatura, para o 403 sair antes do 404.
@router.get("/{tarefa_id}", response_model=TarefaSaida)
def ver_tarefa(usuario=Depends(exigir_permissao("tarefas:ver")), tarefa=Depends(tarefa_existente)):
    return tarefa
