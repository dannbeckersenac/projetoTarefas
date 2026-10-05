# Repositório de itens do checklist. Aula 6 (slide 46): a lista itens = [] saiu,
# e o item passou a morar na tabela itens_checklist.
# Não existe mais listar_por_tarefa: o serviço lê tarefa.itens, pelo relationship.
from modelos.item import ItemChecklist


# INSERT do item. O mesmo commit também grava a tarefa que a regra mudou,
# porque a tarefa veio desta mesma sessão (pela tarefa_existente da rota).
# Item e tarefa vão juntos para o banco, ou nenhum dos dois: isso é uma transação.
def salvar(sessao, dados: dict):
    item = ItemChecklist(**dados)
    sessao.add(item)
    sessao.commit()          # grava o item e a tarefa que a regra mudou
    sessao.refresh(item)
    return item
