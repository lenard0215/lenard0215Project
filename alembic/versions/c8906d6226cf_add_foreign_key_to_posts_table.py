"""add foreign-key to posts table

Revision ID: c8906d6226cf
Revises: a8316303d42b
Create Date: 2024-03-27 10:25:03.613909

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c8906d6226cf'
down_revision: Union[str, None] = 'a8316303d42b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key('post_user_fk', source_table="post", referent_table="users",
                          local_cols=['owner_id'], remote_cols=['id'],ondelete="CASCADE" )
    pass


def downgrade():
    op.drop_constraint('post_users_fk', table_name="posts")
    op.drop_column('posts', 'owner_id')
    pass
