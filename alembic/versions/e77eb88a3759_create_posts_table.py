"""create posts table

Revision ID: e77eb88a3759
Revises: 
Create Date: 2023-02-03 14:46:55.054787

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e77eb88a3759'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'posts', sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
        sa.Column('title', sa.String(), nullable=False),
        sa.Column('content', sa.String(), nullable=False)
    )
    pass


def downgrade() -> None:
    op.drop_table('posts')
    pass
