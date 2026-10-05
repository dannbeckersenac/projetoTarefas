# Esquemas Pydantic da tarefa: conferem o que entra e moldam o que sai da API.
from datetime import date

from pydantic import BaseModel, Field


# Entrada do POST /tarefas. Sem id, situacao e itens_feitos: quem define é o serviço.
class TarefaCriar(BaseModel):
    titulo: str = Field(min_length=3, max_length=100)  # os mesmos tamanhos das colunas no banco
    descricao: str = Field(max_length=500)
    prazo: date                                        # o Pydantic exige o formato AAAA-MM-DD
    solicitante_id: int


# Saída das rotas. Aula 6: o que sai do repositório agora é um objeto Tarefa
# (modelo do SQLAlchemy), e o response_model lê os campos dele pelo ponto.
class TarefaSaida(BaseModel):
    id: int
    titulo: str
    descricao: str
    prazo: date
    situacao: str
    itens_feitos: int
    solicitante_id: int
