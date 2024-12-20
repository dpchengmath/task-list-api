"""Adds is_complete model

Revision ID: ad18d4bf5432
Revises: 94a5ec90b04d
Create Date: 2024-11-02 00:53:15.883838

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ad18d4bf5432'
down_revision = '94a5ec90b04d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('task', schema=None) as batch_op:
        batch_op.add_column(sa.Column('is_complete', sa.Boolean(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('task', schema=None) as batch_op:
        batch_op.drop_column('is_complete')

    # ### end Alembic commands ###
