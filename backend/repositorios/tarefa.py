# Repositório de tarefas. Aula 6: as mesmas funções do ciclo 1, com o corpo novo.
#
# Antes (ciclo 1), a lista vivia dentro do servidor e sumia a cada Ctrl+C ou Ctrl+S:
#     tarefas = []
#     def salvar(tarefa: dict):
#         tarefa["id"] = len(tarefas) + 1
#         tarefas.append(tarefa)
#         return tarefa
#
# Agora quem guarda é o MySQL, e o SQLAlchemy escreve o SQL por nós.
# Repare: as funções devolvem objetos Tarefa, não mais dicionários.
from sqlalchemy import select

from banco import Sessao
from modelos.tarefa import Tarefa


# SELECT de todas as linhas da tabela tarefas, já como objetos Tarefa (slide 25).
def listar():
    sessao = Sessao()                                # abre a conversa, como o abrir_conexao()
    tarefas = sessao.scalars(select(Tarefa)).all()   # SELECT * FROM tarefas
    sessao.close()                                   # fecha a conversa, como o conexao.close()
    return tarefas


# SELECT de uma tarefa pela chave primária. Devolve None se não existir.
def buscar_por_id(tarefa_id: int):
    sessao = Sessao()
    tarefa = sessao.get(Tarefa, tarefa_id)           # SELECT ... WHERE id = tarefa_id
    sessao.close()
    return tarefa


# INSERT de uma tarefa nova (slide 26).
def salvar(dados: dict):
    sessao = Sessao()
    tarefa = Tarefa(**dados)    # o ** da aula 3: o dicionário vira objeto
    sessao.add(tarefa)          # entra na conversa (ainda não foi para o banco)
    sessao.commit()             # o INSERT acontece aqui
    sessao.refresh(tarefa)      # traz de volta o id gerado pelo AUTO_INCREMENT
    sessao.close()
    return tarefa
