# Este router agrupa os endpoints de itens do checklist, que serão adicionados nos planos aprovados.
from fastapi import APIRouter

router = APIRouter(prefix="/tarefas", tags=["itens"])
