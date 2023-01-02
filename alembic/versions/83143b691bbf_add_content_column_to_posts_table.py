"""add content column to posts table

Revision ID: 83143b691bbf
Revises: 0f9cb7a8372d
Create Date: 2022-12-31 16:05:41.488158

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '83143b691bbf'
down_revision = '0f9cb7a8372d'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(),nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts','content')
    pass
    
