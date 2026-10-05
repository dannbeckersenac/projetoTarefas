# Repositório de itens do checklist.
# No primeiro tempo da aula 6, só a tarefa foi para o banco: os itens continuam
# numa lista em memória e somem quando o servidor reinicia. Vão para o MySQL depois do intervalo.
itens = []


# Devolve só os itens da tarefa pedida.
def listar_por_tarefa(tarefa_id: int):
    return [item for item in itens if item["tarefa_id"] == tarefa_id]


# Gera o id com len(lista) + 1 e guarda o item na lista.
def salvar(item: dict):
    item["id"] = len(itens) + 1
    itens.append(item)
    return item
