"""empty message

Revision ID: 1f134abd84f
Revises: 115b85e35c7
Create Date: 2014-07-09 20:32:47.559030

"""

# revision identifiers, used by Alembic.
revision = '1f134abd84f'
down_revision = '115b85e35c7'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('about',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('body', sa.Text(), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('about')
    ### end Alembic commands ###
