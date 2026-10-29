# Aula 6 · A tabela nasce do modelo (slides 23 e 43).
# Rode à mão, na pasta backend/: python criar_tabelas.py
# Substitui o CREATE TABLE escrito à mão no MySQL.
from banco import Base, engine

# Um import por modelo: o import apresenta o modelo para a Base.
# Modelo que não foi importado aqui não vira tabela.
from modelos.grupo import Grupo, Permissao   # Aula 10 · grupos: cria grupos, permissoes e grupo_permissoes
from modelos.usuario import Usuario
from modelos.tarefa import Tarefa
from modelos.item import ItemChecklist

# Cria só as tabelas que ainda não existem. Tabela que já existe não é alterada.
Base.metadata.create_all(engine)

print("Tabelas:", list(Base.metadata.tables))

# Depois de rodar, cadastre no MySQL os usuários da lista fixa, na mesma ordem,
# para os ids baterem com repositorios/usuario.py (e a FK da tarefa aceitar):
# Aula 10 · grupos: o tipo virou grupo_id (1 = solicitante, 2 = executor). Antes:
#   INSERT INTO usuarios (nome, tipo) VALUES ('Júlia', 'solicitante'), ...
# O create_all cria as tabelas de grupos vazias. As linhas dos grupos e das
# permissões vêm da migration criado_grupos_e_permissoes ("alembic upgrade head").
#   INSERT INTO usuarios (nome, grupo_id, email, senha) VALUES
#     ('Júlia', 1, ...), ('Marcos', 2, ...), ('Paulo', 1, ...);
# Confira a ligação com: SHOW CREATE TABLE itens_checklist;  (aparece FOREIGN KEY)
