# Esquemas Pydantic do item do checklist.
from datetime import date

from pydantic import BaseModel, Field


# Entrada do POST /tarefas/{tarefa_id}/itens.
# Sem tarefa_id (vem do caminho) e sem data (o serviço preenche com o dia de hoje).
class ItemCriar(BaseModel):
    tipo: str = Field(pattern="^(etapa|conclusao)$")  # pattern: só aceita um destes dois textos
    descricao: str = Field(min_length=3, max_length=200)


class ItemSaida(BaseModel):
    id: int
    tarefa_id: int
    tipo: str
    descricao: str
    data: date
