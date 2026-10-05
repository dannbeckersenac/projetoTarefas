# Aula 6 · A tabela nasce do modelo (slide 23).
# Rode uma vez, na pasta backend/: python criar_tabelas.py
# Substitui o CREATE TABLE escrito à mão no MySQL.
from banco import Base, engine
from modelos.tarefa import Tarefa  # o import apresenta o modelo para a Base

# Cria só a tabela que ainda não existe. Tabela que já existe não é alterada.
Base.metadata.create_all(engine)

print("Tabelas:", list(Base.metadata.tables))
