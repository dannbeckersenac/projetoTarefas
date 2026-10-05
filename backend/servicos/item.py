# Serviço de itens: a regra da cartilha mora aqui.
from datetime import date

from esquemas.item import ItemCriar
from repositorios import item as repositorio


# Lança um item no checklist aplicando a regra:
# - tarefa concluída recusa item novo;
# - "etapa" soma 1 em itens_feitos e muda a situação para "em andamento";
# - "conclusao" muda a situação para "concluida", sem mexer no contador.
def lancar(sessao, tarefa, dados: ItemCriar):
    # A tarefa é um objeto Tarefa, então é tarefa.situacao, e não tarefa["situacao"].
    if tarefa.situacao == "concluida":
        return "Tarefa já concluída"

    # Atualizar é mudar o atributo do objeto. Não existe comando de UPDATE:
    # a sessão anota o que mudou e grava no próximo commit (slide 40).
    if dados.tipo == "etapa":
        tarefa.itens_feitos += 1
        tarefa.situacao = "em andamento"
    else:
        tarefa.situacao = "concluida"

    item = dados.model_dump()
    item["tarefa_id"] = tarefa.id    # vem do caminho da rota, não do corpo
    item["data"] = date.today()      # preenchida pelo serviço com o dia de hoje

    # Slide 45: um commit só. No passo 3 a tarefa era gravada antes, com
    # repositorio_tarefa.atualizar(sessao, tarefa), e o item depois: dois commits,
    # duas chances de gravar metade. Agora o salvar do item grava os dois juntos.
    #
    # Slide 47, teste do rollback: descomente a linha abaixo, rode a regra pelo /docs
    # (volta 500) e veja que a tarefa não mudou. A sessão fechou sem commit = rollback.
    # raise ValueError("teste do rollback")   # erro depois de mudar a tarefa
    return repositorio.salvar(sessao, item)


# Lista os itens de uma tarefa pelo relationship (slide 42): um ponto vira um SELECT.
def listar(tarefa):
    return tarefa.itens
