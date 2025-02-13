"""Update view_count field

Revision ID: fbe42782779a
Revises: 31806caf242f
Create Date: 2025-02-11 18:35:28.185060

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fbe42782779a'
down_revision = '31806caf242f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('achievements', schema=None) as batch_op:
        batch_op.alter_column('view_count',
               existing_type=sa.INTEGER(),
               nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('achievements', schema=None) as batch_op:
        batch_op.alter_column('view_count',
               existing_type=sa.INTEGER(),
               nullable=True)

    # ### end Alembic commands ###
