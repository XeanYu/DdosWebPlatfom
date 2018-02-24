"""empty message

Revision ID: 0661bee0bc99
Revises: 
Create Date: 2018-01-29 12:55:34.382148

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0661bee0bc99'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('login_logs', sa.Column('login_date', sa.String(length=64), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('login_logs', 'login_date')
    # ### end Alembic commands ###
