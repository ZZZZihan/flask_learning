"""add new fields to achievement model

Revision ID: 31806caf242f
Revises: 623accb8cd92
Create Date: 2025-02-11 17:47:53.619810

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '31806caf242f'
down_revision = '623accb8cd92'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('achievements', schema=None) as batch_op:
        batch_op.add_column(sa.Column('abstract', sa.Text(), nullable=True))
        batch_op.add_column(sa.Column('keywords', sa.String(length=200), nullable=True))
        batch_op.add_column(sa.Column('status', sa.String(length=20), nullable=True))
        batch_op.add_column(sa.Column('view_count', sa.Integer(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('achievements', schema=None) as batch_op:
        batch_op.drop_column('view_count')
        batch_op.drop_column('status')
        batch_op.drop_column('keywords')
        batch_op.drop_column('abstract')

    # ### end Alembic commands ###
