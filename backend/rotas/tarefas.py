# Rotas de tarefas e dos itens do checklist. Aqui só entra HTTP: status, HTTPException e esquemas.
# Na aula 6 (primeiro tempo) as rotas não mudaram: a troca para o banco ficou toda no repositório.
from fastapi import APIRouter, Depends, HTTPException

from esquemas.item import ItemCriar, ItemSaida
from esquemas.tarefa import TarefaCriar, TarefaSaida
from servicos import item as servico_item
from servicos import tarefa as servico

router = APIRouter(prefix="/tarefas", tags=["tarefas"])


# Dependência da aula 4: toda rota com tarefa_id passa por aqui.
# Devolve a tarefa (agora um objeto vindo do MySQL) ou levanta o 404.
def tarefa_existente(tarefa_id: int):
    tarefa = servico.buscar_por_id(tarefa_id)
    if tarefa is None:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    return tarefa


# Abre uma tarefa. 201 com a tarefa criada, já com o id que o banco gerou.
@router.post("", response_model=TarefaSaida, status_code=201)
def criar_tarefa(dados: TarefaCriar):
    resultado = servico.criar(dados)
    # O serviço devolve texto quando recusa: solicitante inexistente vira 422.
    if isinstance(resultado, str):
        raise HTTPException(status_code=422, detail=resultado)
    return resultado


# Lista as tarefas, com os filtros opcionais por situação e por solicitante.
@router.get("", response_model=list[TarefaSaida])
def listar_tarefas(situacao: str | None = None, solicitante_id: int | None = None):
    return servico.listar(situacao, solicitante_id)


# Mostra uma tarefa. O Depends já resolveu o 404 antes de chegar aqui.
@router.get("/{tarefa_id}", response_model=TarefaSaida)
def ver_tarefa(tarefa=Depends(tarefa_existente)):
    return tarefa


# Lança um item no checklist. 409 quando a tarefa já está concluída.
@router.post("/{tarefa_id}/itens", response_model=ItemSaida, status_code=201)
def lancar_item(dados: ItemCriar, tarefa=Depends(tarefa_existente)):
    resultado = servico_item.lancar(tarefa, dados)
    if isinstance(resultado, str):
        raise HTTPException(status_code=409, detail=resultado)
    return resultado


# Lista os itens do checklist de uma tarefa.
@router.get("/{tarefa_id}/itens", response_model=list[ItemSaida])
def listar_itens(tarefa=Depends(tarefa_existente)):
    return servico_item.listar(tarefa)
