# Rotas dos itens do checklist. Aqui só entra HTTP: status, HTTPException e esquemas.
# A dependência tarefa_existente mora em rotas/tarefas.py e é reaproveitada aqui.
# Na mesma requisição, o FastAPI entrega a MESMA sessão para a dependência e para a rota.
from fastapi import APIRouter, Depends, HTTPException

from banco import obter_sessao
from esquemas.item import ItemCriar, ItemSaida
from rotas.autenticacao import exigir_permissao   # Aula 10 · grupos: no lugar do obter_usuario_atual
from rotas.tarefas import tarefa_existente
from servicos import item as servico

router = APIRouter(prefix="/tarefas", tags=["itens"])


# Lança um item no checklist. 409 quando a tarefa já está concluída.
# Aula 10 · grupos: só o grupo executor tem "itens:lancar". A permissão vem primeiro
# na assinatura: solicitante recebe 403 antes de a tarefa ser buscada.
@router.post("/{tarefa_id}/itens", response_model=ItemSaida, status_code=201)
def lancar_item(dados: ItemCriar, usuario=Depends(exigir_permissao("itens:lancar")),
                tarefa=Depends(tarefa_existente), sessao=Depends(obter_sessao)):
    resultado = servico.lancar(sessao, tarefa, dados)
    if isinstance(resultado, str):
        raise HTTPException(status_code=409, detail=resultado)
    return resultado


# Lista os itens do checklist de uma tarefa.
# Aula 10 · grupos: os dois grupos têm "itens:listar". A solicitante só chega aos itens
# das tarefas dela, porque o tarefa_existente devolve 404 para as tarefas de outra pessoa.
@router.get("/{tarefa_id}/itens", response_model=list[ItemSaida])
def listar_itens(usuario=Depends(exigir_permissao("itens:listar")),
                 tarefa=Depends(tarefa_existente)):
    return servico.listar(tarefa)
