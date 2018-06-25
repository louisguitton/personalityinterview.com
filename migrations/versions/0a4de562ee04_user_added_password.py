"""user added password

Revision ID: 0a4de562ee04
Revises: 7ed89945ee36
Create Date: 2018-06-25 22:14:27.022080

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0a4de562ee04'
down_revision = '7ed89945ee36'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('password_hash', sa.String(length=128), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'password_hash')
    # ### end Alembic commands ###
