"""update migration

Revision ID: 08167b9aac0a
Revises: bfe7b7972a3e
Create Date: 2022-03-10 14:42:37.610518

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '08167b9aac0a'
down_revision = 'bfe7b7972a3e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('cards', sa.Column('source_id', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('cards', 'source_id')
    # ### end Alembic commands ###
