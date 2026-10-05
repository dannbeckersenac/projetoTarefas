# Aula 6 · O item aponta para a tarefa (slide 41).
from sqlalchemy import Column, Date, ForeignKey, Integer, String

from banco import Base
from modelos.tarefa import Tarefa  # o modelo com ForeignKey importa o modelo para onde ela aponta


class ItemChecklist(Base):
    __tablename__ = "itens_checklist"

    id = Column(Integer, primary_key=True)
    tipo = Column(String(20), nullable=False)          # "etapa" ou "conclusao"
    descricao = Column(String(200), nullable=False)
    data = Column(Date, nullable=False)
    # FOREIGN KEY: o banco só aceita o id de uma tarefa que existe.
    # "tarefas.id" é tabela ponto coluna, com o nome do __tablename__, não o da classe.
    tarefa_id = Column(Integer, ForeignKey("tarefas.id"), nullable=False)
