"""add content table to posts table

Revision ID: aa8b63087368
Revises: eb24443ff315
Create Date: 2024-03-27 09:56:22.920748

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'aa8b63087368'
down_revision: Union[str, None] = 'eb24443ff315'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_column('post', 'content')
    pass
