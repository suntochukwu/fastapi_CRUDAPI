"""add user table

Revision ID: f11b008dc991
Revises: 83143b691bbf
Create Date: 2023-01-01 20:23:15.301309

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f11b008dc991'
down_revision = '83143b691bbf'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('users', 
    sa.Column('id',sa.Integer, primary_key=True, nullable=False),
    sa.Column('email',sa.String,nullable=False, unique=True),
    sa.Column('password',sa.String,nullable=False),
    sa.Column('created_at',sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('now()')),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
                        )
    pass


def downgrade() -> None:
    op.drop_table('users')
    pass
