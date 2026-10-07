# Rotas de tarefas. Aqui só entra HTTP: status, HTTPException e esquemas.
# Aula 6 (slides 37 e 38): toda rota que chega ao banco pede a sessão com
# sessao=Depends(obter_sessao) e passa adiante: rota, serviço, repositório.
# O FastAPI abre a sessão quando a requisição chega e fecha quando a resposta sai.
from fastapi import APIRouter, Depends, HTTPException, Query

from banco import obter_sessao
from esquemas.tarefa import TarefaCriar, TarefaSaida
from servicos import tarefa as servico

router = APIRouter(prefix="/tarefas", tags=["tarefas"])


# Dependência da aula 4: toda rota com tarefa_id passa por aqui.
# Aula 6: ela também pede a sessão. Na mesma requisição, o FastAPI entrega a MESMA
# sessão para a dependência e para a rota. Por isso, quando a regra muda a tarefa,
# o commit do item sabe o que mudou.
def tarefa_existente(tarefa_id: int, sessao=Depends(obter_sessao)):
    tarefa = servico.buscar_por_id(sessao, tarefa_id)
    if tarefa is None:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    return tarefa


# Abre uma tarefa. 201 com a tarefa criada, já com o id que o banco gerou.
@router.post("", response_model=TarefaSaida, status_code=201)
def criar_tarefa(dados: TarefaCriar, sessao=Depends(obter_sessao)):
    resultado = servico.criar(sessao, dados)
    # O serviço devolve texto quando recusa: solicitante inexistente vira 422.
    if isinstance(resultado, str):
        raise HTTPException(status_code=422, detail=resultado)
    return resultado


# Lista as tarefas, com os filtros opcionais e a página.
# Query(default=1, ge=1): sem página na URL, vale 1; o ge (maior ou igual) é o mesmo
# do Field, então pagina=0 volta 422 antes de chegar ao serviço.
@router.get("", response_model=list[TarefaSaida])
def listar_tarefas(
    situacao: str | None = None,
    solicitante_id: int | None = None,
    pagina: int = Query(default=1, ge=1),
    sessao=Depends(obter_sessao),
):
    return servico.listar(sessao, situacao, solicitante_id, pagina)


# Mostra uma tarefa. O Depends já resolveu o 404 antes de chegar aqui.
@router.get("/{tarefa_id}", response_model=TarefaSaida)
def ver_tarefa(tarefa=Depends(tarefa_existente)):
    return tarefa
