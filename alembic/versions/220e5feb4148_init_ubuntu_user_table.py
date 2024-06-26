"""init-ubuntu-user-table

Revision ID: 220e5feb4148
Revises: f7781712aa5b
Create Date: 2024-05-14 01:41:51.653481

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '220e5feb4148'
down_revision: Union[str, None] = 'f7781712aa5b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('ubuntu_user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(), nullable=False),
    sa.Column('added_at', sa.TIMESTAMP(), nullable=True),
    sa.Column('password', sa.String(length=1024), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_ubuntu_user_id'), 'ubuntu_user', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_ubuntu_user_id'), table_name='ubuntu_user')
    op.drop_table('ubuntu_user')
    # ### end Alembic commands ###
