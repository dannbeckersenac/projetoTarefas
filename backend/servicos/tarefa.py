# Serviço de tarefas: as decisões da cartilha. Nada de HTTPException nem status code aqui.
# Quando recusa, devolve um texto com o motivo, e a rota escolhe o status.
# Aula 6 (slide 38): a sessão chega da rota como primeiro parâmetro e segue para o repositório.
# O serviço não importa modelo nem chama métodos da sessão: isso é do repositório.
from esquemas.tarefa import TarefaCriar
from repositorios import tarefa as repositorio
from servicos.usuario import tem_permissao   # Aula 10 · grupos: a pergunta "o grupo pode?"


# Abre uma tarefa: define os campos que a requisição não manda.
# Aula 9: o usuário chega da rota, já identificado pelo token. Não precisa mais buscar no banco.
# Aula 10 · grupos: a checagem do tipo saiu. A rota só deixa entrar quem tem "tarefas:criar",
# então quem chega aqui pode abrir tarefa, e o serviço não devolve mais texto. Antes:
#     if usuario.tipo != "solicitante":
#         return "Só a solicitante pode abrir tarefa"
def criar(sessao, dados: TarefaCriar, usuario):
    tarefa = dados.model_dump()      # o esquema vira dicionário
    tarefa["solicitante_id"] = usuario.id   # o dono é quem fez login
    tarefa["situacao"] = "aberta"    # toda tarefa nova nasce aberta
    tarefa["itens_feitos"] = 0       # e com o contador zerado
    return repositorio.salvar(sessao, tarefa)


# Lista as tarefas. Aula 6 (slide 49): o filtro desceu para o repositório, que monta o
# WHERE. O serviço só repassa. A compreensão de lista que filtrava em Python saiu:
#     [t for t in tarefas if t.situacao == situacao]
# Aula 10 · grupos: quem não tem "tarefas:ver_todas" (a solicitante) só vê as próprias tarefas.
# O solicitante_id da URL é trocado pelo id de quem fez login: mesmo pedindo
# ?solicitante_id=3, a Júlia recebe só as dela. O executor continua filtrando à vontade.
def listar(sessao, situacao: str | None, solicitante_id: int | None, pagina: int, usuario):
    if not tem_permissao(usuario, "tarefas:ver_todas"):
        solicitante_id = usuario.id
    return repositorio.listar(sessao, situacao, solicitante_id, pagina)


# Busca uma tarefa. Devolve None quando não existe; a rota transforma isso em 404.
# Aula 10 · grupos: também devolve None quando a tarefa é de outra pessoa e o grupo
# não tem "tarefas:ver_todas". Para quem pergunta, as duas situações parecem iguais.
def buscar_por_id(sessao, tarefa_id: int, usuario):
    tarefa = repositorio.buscar_por_id(sessao, tarefa_id)
    if tarefa is None:
        return None
    if tarefa.solicitante_id != usuario.id and not tem_permissao(usuario, "tarefas:ver_todas"):
        return None
    return tarefa
