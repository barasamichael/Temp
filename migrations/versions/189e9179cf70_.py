"""empty message

Revision ID: 189e9179cf70
Revises: 942b9c70506d
Create Date: 2023-11-15 06:26:13.311760

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '189e9179cf70'
down_revision = '942b9c70506d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('books', schema=None) as batch_op:
        batch_op.add_column(sa.Column('isSuspended', sa.Boolean(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('books', schema=None) as batch_op:
        batch_op.drop_column('isSuspended')

    # ### end Alembic commands ###
