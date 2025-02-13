"""add tech_summaries table

Revision ID: 623accb8cd92
Revises: c6f1621a356a
Create Date: 2025-02-05 18:37:14.034933

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '623accb8cd92'
down_revision = 'c6f1621a356a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('tech_summaries',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=200), nullable=False),
    sa.Column('content', sa.Text(), nullable=False),
    sa.Column('tags', sa.String(length=100), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('author_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['author_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('tech_summaries')
    # ### end Alembic commands ###
