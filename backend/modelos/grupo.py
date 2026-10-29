# Aula 10 · grupos: as tabelas do controle de acesso (RBAC: acesso por papel).
# A ideia: o usuário não recebe permissão uma a uma. Ele entra num GRUPO,
# e o grupo é quem tem a lista de PERMISSÕES. Trocar o que um grupo pode fazer
# é mexer em linhas do banco, sem mudar o código das rotas.
#
#     usuarios ──grupo_id──► grupos ◄──── grupo_permissoes ────► permissoes
#        (N)                  (1)          (a tabela do meio)
from sqlalchemy import Column, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship

from banco import Base


# Aula 10 · grupos: a tabela do meio de um relacionamento N:N (muitos para muitos).
# Um grupo tem várias permissões, e uma permissão aparece em vários grupos.
# Ela não vira classe: só guarda os pares (grupo_id, permissao_id).
# As duas colunas juntas formam a chave primária, então o mesmo par não entra duas vezes.
grupo_permissoes = Table(
    "grupo_permissoes",
    Base.metadata,
    Column("grupo_id", Integer, ForeignKey("grupos.id", name="fk_grupo_permissoes_grupo"), primary_key=True),
    Column("permissao_id", Integer, ForeignKey("permissoes.id", name="fk_grupo_permissoes_permissao"), primary_key=True),
)


# Aula 10 · grupos: cada linha é uma ação da API, como "tarefas:criar".
# O nome segue o padrão recurso:ação, e é o texto que a rota pede no exigir_permissao.
class Permissao(Base):
    __tablename__ = "permissoes"

    id = Column(Integer, primary_key=True)
    nome = Column(String(50), nullable=False, unique=True)   # o UNIQUE vira uq_permissao_nome na migration
    descricao = Column(String(200), nullable=False)          # para quem lê a tabela entender a permissão


# Aula 10 · grupos: cada persona do projeto é um grupo, "solicitante" ou "executor".
class Grupo(Base):
    __tablename__ = "grupos"

    id = Column(Integer, primary_key=True)
    nome = Column(String(20), nullable=False, unique=True)   # o UNIQUE vira uq_grupo_nome na migration

    # Aula 10 · grupos: o secondary diz que o caminho passa pela tabela do meio.
    # grupo.permissoes devolve a lista de objetos Permissao do grupo. Por baixo:
    #   SELECT permissoes.* FROM permissoes
    #   JOIN grupo_permissoes ON permissoes.id = grupo_permissoes.permissao_id
    #   WHERE grupo_permissoes.grupo_id = <id deste grupo>
    permissoes = relationship("Permissao", secondary=grupo_permissoes)
