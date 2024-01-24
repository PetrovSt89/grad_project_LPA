"""model UserBox field wishes creation

Revision ID: 916ddaab71f2
Revises: 545ac50dff89
Create Date: 2024-01-23 22:02:24.624721

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '916ddaab71f2'
down_revision: Union[str, None] = '545ac50dff89'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user_boxes', sa.Column('wishes', sa.Text(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user_boxes', 'wishes')
    # ### end Alembic commands ###