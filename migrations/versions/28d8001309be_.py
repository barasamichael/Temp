"""empty message

Revision ID: 28d8001309be
Revises: 5b185544bda7
Create Date: 2023-11-14 08:56:50.337431

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '28d8001309be'
down_revision = '5b185544bda7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('authors', schema=None) as batch_op:
        batch_op.add_column(sa.Column('summary', sa.Text(), nullable=True))

    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('avatarHash', sa.String(length=32), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_column('avatarHash')

    with op.batch_alter_table('authors', schema=None) as batch_op:
        batch_op.drop_column('summary')

    # ### end Alembic commands ###
