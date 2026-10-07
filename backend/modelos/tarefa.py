# Aula 6 · A tabela, em Python (slide 22).
# ORM: classe vira tabela, atributo vira coluna, objeto vira linha.
# Modelo não é esquema: o esquema (esquemas/) confere o que chega na requisição;
# o modelo (modelos/) é a tabela no MySQL.
from sqlalchemy import Column, Date, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from banco import Base
from modelos.usuario import Usuario  # o modelo com ForeignKey importa o modelo para onde ela aponta


class Tarefa(Base):                                   # herda da Base: vira tabela
    __tablename__ = "tarefas"                         # o nome da tabela no MySQL

    id = Column(Integer, primary_key=True)            # INT PRIMARY KEY AUTO_INCREMENT: o banco numera sozinho
    titulo = Column(String(100), nullable=False)      # VARCHAR(100) NOT NULL, o mesmo tamanho do Field
    descricao = Column(String(500), nullable=False)
    prazo = Column(Date, nullable=False)              # DATE NOT NULL: só o dia, sem hora
    situacao = Column(String(20), nullable=False)
    itens_feitos = Column(Integer, nullable=False)
    # FK do DER (slide 6): o banco só aceita o id de um usuário que existe.
    # Aula 7 · passo 3 (slide 12): a tabela criada sem esta FK não muda com o
    # create_all; quem leva a chave ao banco é a migration do Alembic (passo 4).
    # Sem o name, o Alembic avisa que não sabe desfazer a chave.
    solicitante_id = Column(Integer, ForeignKey("usuarios.id", name="fk_tarefa_solicitante"), nullable=False)

    # Slide 42: o atalho no Python para ler os itens com ponto (tarefa.itens).
    # Não cria coluna nenhuma: quem liga as tabelas é a ForeignKey em modelos/item.py.
    # Por baixo: SELECT ... FROM itens_checklist WHERE tarefa_id = <id desta tarefa>
    itens = relationship("ItemChecklist")
