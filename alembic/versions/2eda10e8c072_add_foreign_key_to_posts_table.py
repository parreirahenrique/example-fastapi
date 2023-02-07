"""add foreign key to posts table

Revision ID: 2eda10e8c072
Revises: 4c770c4f6cfe
Create Date: 2023-02-07 08:34:38.562368

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2eda10e8c072'
down_revision = '4c770c4f6cfe'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('user_id', sa.Integer(), nullable=False),)
    op.create_foreign_key('posts_users_fkey', source_table='posts', referent_table='users', local_cols=['user_id'], remote_cols=['id'], ondelete='CASCADE')
    pass


def downgrade() -> None:
    op.drop_constraint('posts_users_fkey', table_name='posts')
    op.drop_column('posts', 'user_id')
    pass
