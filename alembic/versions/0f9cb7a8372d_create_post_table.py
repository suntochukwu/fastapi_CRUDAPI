"""create post table

Revision ID: 0f9cb7a8372d
Revises: 
Create Date: 2022-12-31 15:29:44.727117

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0f9cb7a8372d'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('posts',sa.Column('id',sa.Integer(), nullable= False, primary_key=True), sa.Column('title',sa.String(),nullable=False))
    pass


def downgrade() -> None:
    op.drop_table('posts')
    pass
