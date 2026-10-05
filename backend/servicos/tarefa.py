# Serviço de tarefas: as decisões da cartilha. Nada de HTTPException nem status code aqui.
# Quando recusa, devolve um texto com o motivo, e a rota escolhe o status.
from esquemas.tarefa import TarefaCriar
from repositorios import tarefa as repositorio
from repositorios import usuario as repositorio_usuario


# Abre uma tarefa: confere o solicitante e define os campos que a requisição não manda.
def criar(dados: TarefaCriar):
    solicitante = repositorio_usuario.buscar_por_id(dados.solicitante_id)
    # O usuário ainda é dicionário (lista em memória), por isso o colchete aqui continua.
    if solicitante is None or solicitante["tipo"] != "solicitante":
        return "Solicitante não encontrado"
    tarefa = dados.model_dump()      # o esquema vira dicionário
    tarefa["situacao"] = "aberta"    # toda tarefa nova nasce aberta
    tarefa["itens_feitos"] = 0       # e com o contador zerado
    return repositorio.salvar(tarefa)


# Lista as tarefas, com os dois filtros opcionais da cartilha (slide 27).
# Aula 6: o repositório agora devolve objetos Tarefa, não dicionários.
# t["situacao"] daria TypeError: 'Tarefa' object is not subscriptable (500 na API).
# Por isso o colchete virou ponto: t.situacao.
def listar(situacao: str | None, solicitante_id: int | None):
    tarefas = repositorio.listar()
    if situacao is not None:
        tarefas = [t for t in tarefas if t.situacao == situacao]  # era t["situacao"]
    if solicitante_id is not None:
        tarefas = [t for t in tarefas if t.solicitante_id == solicitante_id]  # era t["solicitante_id"]
    return tarefas


# Busca uma tarefa. Devolve None quando não existe; a rota transforma isso em 404.
def buscar_por_id(tarefa_id: int):
    return repositorio.buscar_por_id(tarefa_id)
