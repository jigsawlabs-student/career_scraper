"""add date posted to positionn.

Revision ID: 764294dc4737
Revises: f97f232a1e4e
Create Date: 2022-03-14 18:02:18.602801

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '764294dc4737'
down_revision = 'f97f232a1e4e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('positions', sa.Column('date_posted', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('positions', 'date_posted')
    # ### end Alembic commands ###
