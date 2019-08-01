"""empty message

Revision ID: 731f0dcaa96d
Revises: bb57336c3900
Create Date: 2019-08-01 16:21:42.673959

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '731f0dcaa96d'
down_revision = 'bb57336c3900'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('transaction', sa.Column('transtype', sa.String(length=255), nullable=True))
    op.create_index(op.f('ix_transaction_transtype'), 'transaction', ['transtype'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_transaction_transtype'), table_name='transaction')
    op.drop_column('transaction', 'transtype')
    # ### end Alembic commands ###
