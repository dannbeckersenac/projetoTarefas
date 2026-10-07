# Rotas dos itens do checklist. Aqui só entra HTTP: status, HTTPException e esquemas.
# A dependência tarefa_existente mora em rotas/tarefas.py e é reaproveitada aqui.
# Na mesma requisição, o FastAPI entrega a MESMA sessão para a dependência e para a rota.
from fastapi import APIRouter, Depends, HTTPException

from banco import obter_sessao
from esquemas.item import ItemCriar, ItemSaida
from rotas.tarefas import tarefa_existente
from servicos import item as servico

router = APIRouter(prefix="/tarefas", tags=["itens"])


# Lança um item no checklist. 409 quando a tarefa já está concluída.
@router.post("/{tarefa_id}/itens", response_model=ItemSaida, status_code=201)
def lancar_item(dados: ItemCriar, tarefa=Depends(tarefa_existente), sessao=Depends(obter_sessao)):
    resultado = servico.lancar(sessao, tarefa, dados)
    if isinstance(resultado, str):
        raise HTTPException(status_code=409, detail=resultado)
    return resultado


# Lista os itens do checklist de uma tarefa.
@router.get("/{tarefa_id}/itens", response_model=list[ItemSaida])
def listar_itens(tarefa=Depends(tarefa_existente)):
    return servico.listar(tarefa)
