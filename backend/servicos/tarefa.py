# Serviço de tarefas: as decisões da cartilha. Nada de HTTPException nem status code aqui.
# Quando recusa, devolve um texto com o motivo, e a rota escolhe o status.
# Aula 6 (slide 38): a sessão chega da rota como primeiro parâmetro e segue para o repositório.
# O serviço não importa modelo nem chama métodos da sessão: isso é do repositório.
from esquemas.tarefa import TarefaCriar
from repositorios import tarefa as repositorio
from repositorios import usuario as repositorio_usuario


# Abre uma tarefa: confere o solicitante e define os campos que a requisição não manda.
def criar(sessao, dados: TarefaCriar):
    solicitante = repositorio_usuario.buscar_por_id(dados.solicitante_id)
    # O usuário ainda vem da lista fixa (dicionário), por isso aqui o colchete continua.
    if solicitante is None or solicitante["tipo"] != "solicitante":
        return "Solicitante não encontrado"
    tarefa = dados.model_dump()      # o esquema vira dicionário
    tarefa["situacao"] = "aberta"    # toda tarefa nova nasce aberta
    tarefa["itens_feitos"] = 0       # e com o contador zerado
    return repositorio.salvar(sessao, tarefa)


# Lista as tarefas. Aula 6 (slide 49): o filtro desceu para o repositório, que monta o
# WHERE. O serviço só repassa. A compreensão de lista que filtrava em Python saiu:
#     [t for t in tarefas if t.situacao == situacao]
def listar(sessao, situacao: str | None, solicitante_id: int | None, pagina: int):
    return repositorio.listar(sessao, situacao, solicitante_id, pagina)


# Busca uma tarefa. Devolve None quando não existe; a rota transforma isso em 404.
def buscar_por_id(sessao, tarefa_id: int):
    return repositorio.buscar_por_id(sessao, tarefa_id)
