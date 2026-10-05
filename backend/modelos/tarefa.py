# Aula 6 · A tabela, em Python (slide 22).
# ORM: classe vira tabela, atributo vira coluna, objeto vira linha.
# Modelo não é esquema: o esquema (esquemas/) confere o que chega na requisição;
# o modelo (modelos/) é a tabela no MySQL.
from sqlalchemy import Column, Date, Integer, String

from banco import Base


class Tarefa(Base):                                   # herda da Base: vira tabela
    __tablename__ = "tarefas"                         # o nome da tabela no MySQL

    id = Column(Integer, primary_key=True)            # INT PRIMARY KEY AUTO_INCREMENT: o banco numera sozinho
    titulo = Column(String(100), nullable=False)      # VARCHAR(100) NOT NULL, o mesmo tamanho do Field
    descricao = Column(String(500), nullable=False)
    prazo = Column(Date, nullable=False)              # DATE NOT NULL: só o dia, sem hora
    situacao = Column(String(20), nullable=False)
    itens_feitos = Column(Integer, nullable=False)
    # Por enquanto só guarda o número de quem pediu. A ligação com a tabela
    # de usuários (ForeignKey) vem no segundo tempo.
    solicitante_id = Column(Integer, nullable=False)
