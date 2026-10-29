# Aula 6 · segundo tempo, passo 4 (slide 43): a tabela usuarios.
# A API continua lendo a lista fixa de repositorios/usuario.py. A tabela existe para
# a ForeignKey da tarefa ter para onde apontar, então ela precisa dos mesmos usuários,
# com os mesmos ids (o INSERT está no criar_tabelas.py).
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from banco import Base
from modelos.grupo import Grupo  # Aula 10 · grupos: o modelo com ForeignKey importa o modelo para onde ela aponta


class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True)
    nome = Column(String(100), nullable=False)
    # Aula 10 · grupos: a coluna tipo saiu. Antes:
    #     tipo = Column(String(20), nullable=False, default="solicitante")   # "solicitante" ou "executor"
    # Agora a persona é uma linha da tabela grupos, e o usuário aponta para ela.
    # Quem leva esta FK ao banco é a migration criado_grupos_e_permissoes.
    grupo_id = Column(Integer, ForeignKey("grupos.id", name="fk_usuario_grupo"), nullable=False)
    plano = Column(String(20), nullable=False, default="gratuito")  # "gratuito" ou "premium"
    email = Column(String(100), nullable=False, unique=True)
    senha = Column(String(255), nullable=False)

    # Aula 10 · grupos: o atalho para ler o grupo com ponto (usuario.grupo.nome).
    # Não cria coluna: quem liga as tabelas é o grupo_id acima.
    grupo = relationship("Grupo")
