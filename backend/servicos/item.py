# Serviço de itens: a regra da cartilha mora aqui.
from datetime import date

from esquemas.item import ItemCriar
from repositorios import item as repositorio


# Lança um item no checklist aplicando a regra:
# - tarefa concluída recusa item novo;
# - "etapa" soma 1 em itens_feitos e muda a situação para "em andamento";
# - "conclusao" muda a situação para "concluida", sem mexer no contador.
def lancar(tarefa, dados: ItemCriar):
    # Aula 6: a tarefa é um objeto Tarefa, então é tarefa.situacao, e não tarefa["situacao"].
    if tarefa.situacao == "concluida":
        return "Tarefa já concluída"

    if dados.tipo == "etapa":
        tarefa.itens_feitos += 1
        tarefa.situacao = "em andamento"
    else:
        tarefa.situacao = "concluida"
    # ATENÇÃO (gancho para o segundo tempo, slides 30 e 31): estas mudanças ficam só no
    # objeto. A sessão que buscou a tarefa já fechou e ninguém faz commit, então o banco
    # não fica sabendo. O GET da tarefa continua "aberta", com 0.

    item = dados.model_dump()
    item["tarefa_id"] = tarefa.id    # vem do caminho da rota, não do corpo
    item["data"] = date.today()      # preenchida pelo serviço com o dia de hoje
    return repositorio.salvar(item)


# Lista os itens de uma tarefa que já sabemos que existe.
def listar(tarefa):
    return repositorio.listar_por_tarefa(tarefa.id)
