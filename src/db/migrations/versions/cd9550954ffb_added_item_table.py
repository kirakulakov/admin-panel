"""added item table

Revision ID: cd9550954ffb
Revises: df7ddf65f304
Create Date: 2023-10-24 15:18:29.969205

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = 'cd9550954ffb'
down_revision = 'df7ddf65f304'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('item',
                    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'),
                              nullable=False),
                    sa.Column('updated_at', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'),
                              nullable=False),
                    sa.Column('account_id', sa.Integer(), nullable=False),
                    sa.Column('name', sa.VARCHAR(length=255), nullable=False),
                    sa.ForeignKeyConstraint(['account_id'], ['users.id'], name=op.f('fk_item_account_id_users'),
                                            ondelete='CASCADE'),
                    sa.PrimaryKeyConstraint('id', name=op.f('pk_item')),
                    sa.UniqueConstraint('id', name=op.f('uq_item_id'))
                    )
    op.create_index(op.f('ix_item_account_id'), 'item', ['account_id'], unique=False)
    op.create_unique_constraint(op.f('uq_users_id'), 'users', ['id'])


def downgrade():
    op.drop_constraint(op.f('uq_users_id'), 'users', type_='unique')
    op.drop_index(op.f('ix_item_account_id'), table_name='item')
    op.drop_table('item')
