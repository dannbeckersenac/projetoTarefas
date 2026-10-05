# Aula 6 · segundo tempo, passo 4 (slide 43): a tabela usuarios.
# A API continua lendo a lista fixa de repositorios/usuario.py. A tabela existe para
# a ForeignKey da tarefa ter para onde apontar, então ela precisa dos mesmos usuários,
# com os mesmos ids (o INSERT está no criar_tabelas.py).
from sqlalchemy import Column, Integer, String

from banco import Base


class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True)
    nome = Column(String(100), nullable=False)
    tipo = Column(String(20), nullable=False)   # "solicitante" ou "executor"
