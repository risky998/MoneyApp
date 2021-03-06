"""empty message

Revision ID: bb57336c3900
Revises: 0a1cb394e461
Create Date: 2019-07-29 20:56:27.586872

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bb57336c3900'
down_revision = '0a1cb394e461'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('transaction',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('date', sa.String(), nullable=True),
    sa.Column('debit', sa.Boolean(), nullable=True),
    sa.Column('amount', sa.Float(), nullable=True),
    sa.Column('description', sa.String(length=255), nullable=True),
    sa.Column('category', sa.String(length=255), nullable=True),
    sa.Column('type', sa.String(length=255), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_transaction_amount'), 'transaction', ['amount'], unique=False)
    op.create_index(op.f('ix_transaction_category'), 'transaction', ['category'], unique=False)
    op.create_index(op.f('ix_transaction_date'), 'transaction', ['date'], unique=False)
    op.create_index(op.f('ix_transaction_debit'), 'transaction', ['debit'], unique=False)
    op.create_index(op.f('ix_transaction_description'), 'transaction', ['description'], unique=False)
    op.create_index(op.f('ix_transaction_type'), 'transaction', ['type'], unique=False)
    op.drop_index('ix_pay_app_transaction_amount', table_name='pay_app_transaction')
    op.drop_index('ix_pay_app_transaction_category', table_name='pay_app_transaction')
    op.drop_index('ix_pay_app_transaction_date', table_name='pay_app_transaction')
    op.drop_index('ix_pay_app_transaction_debit', table_name='pay_app_transaction')
    op.drop_index('ix_pay_app_transaction_description', table_name='pay_app_transaction')
    op.drop_table('pay_app_transaction')
    op.drop_index('ix_bank_transaction_amount', table_name='bank_transaction')
    op.drop_index('ix_bank_transaction_category', table_name='bank_transaction')
    op.drop_index('ix_bank_transaction_date', table_name='bank_transaction')
    op.drop_index('ix_bank_transaction_debit', table_name='bank_transaction')
    op.drop_index('ix_bank_transaction_description', table_name='bank_transaction')
    op.drop_table('bank_transaction')
    op.drop_index('ix_cash_transaction_amount', table_name='cash_transaction')
    op.drop_index('ix_cash_transaction_category', table_name='cash_transaction')
    op.drop_index('ix_cash_transaction_date', table_name='cash_transaction')
    op.drop_index('ix_cash_transaction_debit', table_name='cash_transaction')
    op.drop_index('ix_cash_transaction_description', table_name='cash_transaction')
    op.drop_table('cash_transaction')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('cash_transaction',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('user_id', sa.INTEGER(), nullable=True),
    sa.Column('date', sa.VARCHAR(), nullable=True),
    sa.Column('debit', sa.BOOLEAN(), nullable=True),
    sa.Column('amount', sa.INTEGER(), nullable=True),
    sa.Column('description', sa.VARCHAR(length=255), nullable=True),
    sa.Column('category', sa.VARCHAR(length=255), nullable=True),
    sa.CheckConstraint('debit IN (0, 1)'),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_cash_transaction_description', 'cash_transaction', ['description'], unique=False)
    op.create_index('ix_cash_transaction_debit', 'cash_transaction', ['debit'], unique=False)
    op.create_index('ix_cash_transaction_date', 'cash_transaction', ['date'], unique=False)
    op.create_index('ix_cash_transaction_category', 'cash_transaction', ['category'], unique=False)
    op.create_index('ix_cash_transaction_amount', 'cash_transaction', ['amount'], unique=False)
    op.create_table('bank_transaction',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('user_id', sa.INTEGER(), nullable=True),
    sa.Column('date', sa.VARCHAR(), nullable=True),
    sa.Column('debit', sa.BOOLEAN(), nullable=True),
    sa.Column('amount', sa.INTEGER(), nullable=True),
    sa.Column('description', sa.VARCHAR(length=255), nullable=True),
    sa.Column('category', sa.VARCHAR(length=255), nullable=True),
    sa.CheckConstraint('debit IN (0, 1)'),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_bank_transaction_description', 'bank_transaction', ['description'], unique=False)
    op.create_index('ix_bank_transaction_debit', 'bank_transaction', ['debit'], unique=False)
    op.create_index('ix_bank_transaction_date', 'bank_transaction', ['date'], unique=False)
    op.create_index('ix_bank_transaction_category', 'bank_transaction', ['category'], unique=False)
    op.create_index('ix_bank_transaction_amount', 'bank_transaction', ['amount'], unique=False)
    op.create_table('pay_app_transaction',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('user_id', sa.INTEGER(), nullable=True),
    sa.Column('date', sa.VARCHAR(), nullable=True),
    sa.Column('debit', sa.BOOLEAN(), nullable=True),
    sa.Column('amount', sa.INTEGER(), nullable=True),
    sa.Column('description', sa.VARCHAR(length=255), nullable=True),
    sa.Column('category', sa.VARCHAR(length=255), nullable=True),
    sa.CheckConstraint('debit IN (0, 1)'),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_pay_app_transaction_description', 'pay_app_transaction', ['description'], unique=False)
    op.create_index('ix_pay_app_transaction_debit', 'pay_app_transaction', ['debit'], unique=False)
    op.create_index('ix_pay_app_transaction_date', 'pay_app_transaction', ['date'], unique=False)
    op.create_index('ix_pay_app_transaction_category', 'pay_app_transaction', ['category'], unique=False)
    op.create_index('ix_pay_app_transaction_amount', 'pay_app_transaction', ['amount'], unique=False)
    op.drop_index(op.f('ix_transaction_type'), table_name='transaction')
    op.drop_index(op.f('ix_transaction_description'), table_name='transaction')
    op.drop_index(op.f('ix_transaction_debit'), table_name='transaction')
    op.drop_index(op.f('ix_transaction_date'), table_name='transaction')
    op.drop_index(op.f('ix_transaction_category'), table_name='transaction')
    op.drop_index(op.f('ix_transaction_amount'), table_name='transaction')
    op.drop_table('transaction')
    # ### end Alembic commands ###
