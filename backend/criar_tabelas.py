# Aula 6 · A tabela nasce do modelo (slides 23 e 43).
# Rode à mão, na pasta backend/: python criar_tabelas.py
# Substitui o CREATE TABLE escrito à mão no MySQL.
from banco import Base, engine

# Um import por modelo: o import apresenta o modelo para a Base.
# Modelo que não foi importado aqui não vira tabela.
from modelos.usuario import Usuario
from modelos.tarefa import Tarefa
from modelos.item import ItemChecklist

# Cria só as tabelas que ainda não existem. Tabela que já existe não é alterada.
Base.metadata.create_all(engine)

print("Tabelas:", list(Base.metadata.tables))

# Depois de rodar, cadastre no MySQL os usuários da lista fixa, na mesma ordem,
# para os ids baterem com repositorios/usuario.py (e a FK da tarefa aceitar):
#   INSERT INTO usuarios (nome, tipo) VALUES
#     ('Júlia', 'solicitante'), ('Marcos', 'executor'), ('Paulo', 'solicitante');
# Confira a ligação com: SHOW CREATE TABLE itens_checklist;  (aparece FOREIGN KEY)
