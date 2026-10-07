"""adicionado email e senha no usuario

Revision ID: 51b1e88d2cc1
Revises: 8f4995617a40
Create Date: 2026-10-07 19:38:48.834099

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '51b1e88d2cc1'
down_revision: Union[str, Sequence[str], None] = '8f4995617a40'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


# Usuários que já estão na tabela: id -> (email, senha).
# ATENÇÃO: senha gravada em TEXTO PURO, de propósito, para simular o problema.
# Quem ler a tabela (SELECT * FROM usuarios) vê a senha de todo mundo.
usuarios_existentes = {
    1: ("julia@tarefacerta.com", "julia123"),
    2: ("marcos@tarefacerta.com", "marcos123"),
    3: ("paulo@tarefacerta.com", "paulo123"),
    4: ("fernanda@tarefacerta.com", "fernanda123"),
    5: ("ricardo@tarefacerta.com", "ricardo123"),
}


def upgrade() -> None:
    """Upgrade schema."""
    # 1. A tabela já tem linhas: coluna NOT NULL sem valor quebraria o ALTER.
    #    Por isso as colunas nascem aceitando NULL.
    op.add_column('usuarios', sa.Column('email', sa.String(length=100), nullable=True))
    op.add_column('usuarios', sa.Column('senha', sa.String(length=255), nullable=True))

    # 2. Preenche email e senha dos usuários existentes.
    usuarios = sa.table('usuarios', sa.column('id', sa.Integer), sa.column('email', sa.String), sa.column('senha', sa.String))
    for usuario_id, (email, senha) in usuarios_existentes.items():
        op.execute(
            usuarios.update()
            .where(usuarios.c.id == usuario_id)
            .values(email=email, senha=senha)
        )

    # 3. Com todo mundo preenchido, agora sim: NOT NULL e email único.
    op.alter_column('usuarios', 'email', existing_type=sa.String(length=100), nullable=False)
    op.alter_column('usuarios', 'senha', existing_type=sa.String(length=255), nullable=False)
    op.create_unique_constraint('uq_usuario_email', 'usuarios', ['email'])


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint('uq_usuario_email', 'usuarios', type_='unique')
    op.drop_column('usuarios', 'senha')
    op.drop_column('usuarios', 'email')
