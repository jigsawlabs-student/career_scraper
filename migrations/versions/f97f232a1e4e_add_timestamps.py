"""add timestamps

Revision ID: f97f232a1e4e
Revises: 08167b9aac0a
Create Date: 2022-03-11 11:44:43.568138

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f97f232a1e4e'
down_revision = '08167b9aac0a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('cards', sa.Column('timestamp', sa.DateTime(), nullable=True))
    op.add_column('scraped_pages', sa.Column('timestamp', sa.DateTime(), nullable=True))
    op.drop_column('scraped_pages', 'timestamp')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('scraped_pages', 'timestamp')
    op.drop_column('cards', 'timestamp')
    # ### end Alembic commands ###