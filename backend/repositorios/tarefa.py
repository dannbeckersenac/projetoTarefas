# Repositório de tarefas. Aula 6: as mesmas funções do ciclo 1, com o corpo novo.
#
# Ciclo 1: a lista vivia dentro do servidor e sumia a cada Ctrl+C ou Ctrl+S.
#     tarefas = []
#
# Primeiro tempo: cada função abria e fechava a própria conversa.
#     sessao = Sessao()  ...  sessao.close()
# Problema (slide 31): a sessão fechava antes de a regra mudar a tarefa, e a mudança
# nunca chegava ao banco.
#
# Segundo tempo (slide 38): a sessão chega pronta, como primeiro parâmetro, vinda do
# Depends(obter_sessao) da rota. O repositório não abre nem fecha sessão.
# As funções devolvem objetos Tarefa, não dicionários.
from sqlalchemy import select

from modelos.tarefa import Tarefa


# Slide 49: quem filtra, ordena e pagina é o banco. O repositório só monta a consulta.
# Antes, vinha a tabela inteira e o serviço filtrava em Python: mil linhas para sobrar dez.
def listar(sessao, situacao: str | None, solicitante_id: int | None, pagina: int):
    consulta = select(Tarefa).order_by(Tarefa.prazo)            # ORDER BY prazo: o mais perto primeiro
    if situacao is not None:                                    # o filtro só entra se veio
        consulta = consulta.where(Tarefa.situacao == situacao)  # WHERE situacao = 'aberta'
    if solicitante_id is not None:
        consulta = consulta.where(Tarefa.solicitante_id == solicitante_id)
    consulta = consulta.limit(10).offset((pagina - 1) * 10)     # LIMIT 10: dez por página; a página 3 pula 20
    return sessao.scalars(consulta).all()


# SELECT de uma tarefa pela chave primária. Devolve None se não existir.
def buscar_por_id(sessao, tarefa_id: int):
    return sessao.get(Tarefa, tarefa_id)


# INSERT de uma tarefa nova.
def salvar(sessao, dados: dict):
    tarefa = Tarefa(**dados)    # o ** da aula 3: o dicionário vira objeto
    sessao.add(tarefa)          # entra na conversa (ainda não foi para o banco)
    sessao.commit()             # o INSERT acontece aqui
    sessao.refresh(tarefa)      # traz de volta o id gerado pelo AUTO_INCREMENT
    return tarefa
