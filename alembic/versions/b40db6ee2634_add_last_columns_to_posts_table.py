"""add last columns to posts table

Revision ID: b40db6ee2634
Revises: 2eda10e8c072
Create Date: 2023-02-07 08:51:57.550143

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b40db6ee2634'
down_revision = '2eda10e8c072'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('published', sa.Boolean(), server_default='TRUE', nullable=False))
    op.add_column('posts', sa.Column('votes', sa.Integer(), nullable=False, server_default='0'))
    op.add_column('posts', sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('now()')))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'published')
    op.drop_column('posts', 'votes')
    op.drop_column('posts', 'created_at')
    pass
