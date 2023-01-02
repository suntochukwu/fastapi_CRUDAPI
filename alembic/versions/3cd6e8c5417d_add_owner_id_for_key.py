"""add owner id for_key

Revision ID: 3cd6e8c5417d
Revises: f11b008dc991
Create Date: 2023-01-02 05:53:26.523122

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3cd6e8c5417d'
down_revision = 'f11b008dc991'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts',sa.Column('owner_id',sa.Integer(), nullable=False))
    op.create_foreign_key('posts_users_fk', source_table='posts',referent_table='users',local_cols='owner_id',remote_cols='id', ondelete='CASCADE')
    pass



def downgrade() -> None:
    op.drop_constraint('posts_users_fk', table_name='posts')
    op.drop_column('posts','owner_id')
    pass
