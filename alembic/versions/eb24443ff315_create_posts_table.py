"""create posts table

Revision ID: eb24443ff315
Revises: 
Create Date: 2024-03-27 08:21:12.486446

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'eb24443ff315'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table('posts', sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
                    sa.Column('title', sa.Integer(), nullable=False, primary_key=True))
    pass


def downgrade():
    op.drop_table('posts')
    pass
