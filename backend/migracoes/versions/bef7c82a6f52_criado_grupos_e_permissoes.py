"""criado grupos e permissoes

Revision ID: bef7c82a6f52
Revises: 51b1e88d2cc1
Create Date: 2026-10-20 20:49:53.235617

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'bef7c82a6f52'
down_revision: Union[str, Sequence[str], None] = '51b1e88d2cc1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


# Aula 10 · grupos: os dados iniciais. Os ids são fixos de propósito:
# o UPDATE dos usuários (passo 4) usa 1 e 2 para ligar cada tipo antigo ao grupo novo.
grupos_iniciais = [
    {"id": 1, "nome": "solicitante"},
    {"id": 2, "nome": "executor"},
]

# Aula 10 · grupos: uma permissão por ação da API, no padrão recurso:ação.
permissoes_iniciais = [
    {"id": 1, "nome": "tarefas:criar", "descricao": "Abrir tarefa"},
    {"id": 2, "nome": "tarefas:listar", "descricao": "Listar tarefas"},
    {"id": 3, "nome": "tarefas:ver", "descricao": "Ver uma tarefa"},
    {"id": 4, "nome": "tarefas:ver_todas", "descricao": "Ver tarefas de qualquer solicitante"},
    {"id": 5, "nome": "itens:lancar", "descricao": "Lançar item no checklist"},
    {"id": 6, "nome": "itens:listar", "descricao": "Listar itens de uma tarefa"},
    {"id": 7, "nome": "usuarios:listar", "descricao": "Listar usuários"},
    {"id": 8, "nome": "usuarios:ver", "descricao": "Ver um usuário pelo id"},
]

# Aula 10 · grupos: a matriz de acesso. Cada par diz "este grupo tem esta permissão".
# Solicitante (1): abrir, listar e ver as tarefas dela, listar os itens.
# Executor (2): tudo, menos abrir tarefa. E vê as tarefas de todo mundo (ver_todas).
grupo_permissoes_iniciais = [
    {"grupo_id": 1, "permissao_id": 1},
    {"grupo_id": 1, "permissao_id": 2},
    {"grupo_id": 1, "permissao_id": 3},
    {"grupo_id": 1, "permissao_id": 6},
    {"grupo_id": 2, "permissao_id": 2},
    {"grupo_id": 2, "permissao_id": 3},
    {"grupo_id": 2, "permissao_id": 4},
    {"grupo_id": 2, "permissao_id": 5},
    {"grupo_id": 2, "permissao_id": 6},
    {"grupo_id": 2, "permissao_id": 7},
    {"grupo_id": 2, "permissao_id": 8},
]


def upgrade() -> None:
    """Upgrade schema."""
    # Aula 10 · grupos: 1. As três tabelas novas. A do meio vem por último,
    #    porque as FKs dela apontam para as outras duas.
    tabela_grupos = op.create_table(
        'grupos',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('nome', sa.String(length=20), nullable=False),
        sa.UniqueConstraint('nome', name='uq_grupo_nome'),
    )
    tabela_permissoes = op.create_table(
        'permissoes',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('nome', sa.String(length=50), nullable=False),
        sa.Column('descricao', sa.String(length=200), nullable=False),
        sa.UniqueConstraint('nome', name='uq_permissao_nome'),
    )
    tabela_grupo_permissoes = op.create_table(
        'grupo_permissoes',
        sa.Column('grupo_id', sa.Integer(), sa.ForeignKey('grupos.id', name='fk_grupo_permissoes_grupo'), primary_key=True),
        sa.Column('permissao_id', sa.Integer(), sa.ForeignKey('permissoes.id', name='fk_grupo_permissoes_permissao'), primary_key=True),
    )

    # Aula 10 · grupos: 2. Os dados iniciais. O create_table devolve a tabela,
    #    e o bulk_insert faz um INSERT com todas as linhas da lista.
    op.bulk_insert(tabela_grupos, grupos_iniciais)
    op.bulk_insert(tabela_permissoes, permissoes_iniciais)
    op.bulk_insert(tabela_grupo_permissoes, grupo_permissoes_iniciais)

    # Aula 10 · grupos: 3. A tabela usuarios já tem linhas: coluna NOT NULL sem valor
    #    quebraria o ALTER. Por isso grupo_id nasce aceitando NULL (a mesma ideia do email).
    op.add_column('usuarios', sa.Column('grupo_id', sa.Integer(), nullable=True))

    # Aula 10 · grupos: 4. Cada usuário vai para o grupo do tipo que ele tinha.
    op.execute("UPDATE usuarios SET grupo_id = 1 WHERE tipo = 'solicitante'")
    op.execute("UPDATE usuarios SET grupo_id = 2 WHERE tipo = 'executor'")

    # Aula 10 · grupos: 5. Com todo mundo preenchido, agora sim: NOT NULL e a FK.
    op.alter_column('usuarios', 'grupo_id', existing_type=sa.Integer(), nullable=False)
    op.create_foreign_key('fk_usuario_grupo', 'usuarios', 'grupos', ['grupo_id'], ['id'])

    # Aula 10 · grupos: 6. O tipo já foi copiado para grupo_id e pode sair.
    op.drop_column('usuarios', 'tipo')


def downgrade() -> None:
    """Downgrade schema."""
    # Aula 10 · grupos: o caminho de volta, na ordem inversa do upgrade.
    # 1. O tipo volta aceitando NULL e é preenchido a partir do grupo.
    op.add_column('usuarios', sa.Column('tipo', sa.String(length=20), nullable=True))
    op.execute("UPDATE usuarios SET tipo = 'solicitante' WHERE grupo_id = 1")
    op.execute("UPDATE usuarios SET tipo = 'executor' WHERE grupo_id = 2")
    op.alter_column('usuarios', 'tipo', existing_type=sa.String(length=20), nullable=False)

    # Aula 10 · grupos: 2. No MySQL, a FK sai antes da coluna que ela usa.
    op.drop_constraint('fk_usuario_grupo', 'usuarios', type_='foreignkey')
    op.drop_column('usuarios', 'grupo_id')

    # Aula 10 · grupos: 3. A tabela do meio sai primeiro: as FKs dela apontam para as outras.
    op.drop_table('grupo_permissoes')
    op.drop_table('permissoes')
    op.drop_table('grupos')
