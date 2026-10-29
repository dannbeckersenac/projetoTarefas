# Repositório de usuários. A lista fixa saiu: agora os usuários moram na tabela usuarios.
#
# Antes:
#     usuarios = [
#         {"id": 1, "nome": "Júlia", "tipo": "solicitante"},
#         ...
#     ]
#
# Como no repositório de tarefas, a sessão chega pronta, como primeiro parâmetro,
# e as funções devolvem objetos Usuario, não dicionários.
from sqlalchemy import select

from modelos.usuario import Usuario


# SELECT de todos os usuários, em ordem de nome.
def listar(sessao):
    consulta = select(Usuario).order_by(Usuario.nome)
    return sessao.scalars(consulta).all()


# SELECT de um usuário pela chave primária. Devolve None se não existir.
def buscar_por_id(sessao, usuario_id: int):
    return sessao.get(Usuario, usuario_id)


# SELECT de um usuário pelo e-mail. Devolve None se não existir.
def buscar_por_email(sessao, email: str):
    consulta = select(Usuario).where(Usuario.email == email)
    return sessao.scalars(consulta).first()


# INSERT de um usuário novo.
def salvar(sessao, dados: dict):
    usuario = Usuario(**dados)    # o dicionário vira objeto
    sessao.add(usuario)
    sessao.commit()               # o INSERT acontece aqui
    sessao.refresh(usuario)       # traz de volta o id gerado pelo AUTO_INCREMENT
    return usuario
