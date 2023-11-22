"""empty message

Revision ID: 942b9c70506d
Revises: 28d8001309be
Create Date: 2023-11-14 12:29:43.628666

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '942b9c70506d'
down_revision = '28d8001309be'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('author_book',
    sa.Column('authorBookId', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('authorId', sa.Integer(), nullable=True),
    sa.Column('bookId', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['authorId'], ['authors.authorId'], ),
    sa.ForeignKeyConstraint(['bookId'], ['books.bookId'], ),
    sa.PrimaryKeyConstraint('authorBookId')
    )
    op.create_table('category_book',
    sa.Column('categoryBookId', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('categoryId', sa.Integer(), nullable=True),
    sa.Column('bookId', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['bookId'], ['books.bookId'], ),
    sa.ForeignKeyConstraint(['categoryId'], ['categories.categoryId'], ),
    sa.PrimaryKeyConstraint('categoryBookId')
    )
    op.drop_table('category_book_association')
    op.drop_table('author_book_association')
    with op.batch_alter_table('notifications', schema=None) as batch_op:
        batch_op.add_column(sa.Column('name', sa.String(length=64), nullable=False))
        batch_op.drop_column('content')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('notifications', schema=None) as batch_op:
        batch_op.add_column(sa.Column('content', sa.VARCHAR(length=255), nullable=False))
        batch_op.drop_column('name')

    op.create_table('author_book_association',
    sa.Column('author_id', sa.INTEGER(), nullable=True),
    sa.Column('book_id', sa.INTEGER(), nullable=True),
    sa.ForeignKeyConstraint(['author_id'], ['authors.authorId'], ),
    sa.ForeignKeyConstraint(['book_id'], ['books.bookId'], )
    )
    op.create_table('category_book_association',
    sa.Column('category_id', sa.INTEGER(), nullable=True),
    sa.Column('book_id', sa.INTEGER(), nullable=True),
    sa.ForeignKeyConstraint(['book_id'], ['books.bookId'], ),
    sa.ForeignKeyConstraint(['category_id'], ['categories.categoryId'], )
    )
    op.drop_table('category_book')
    op.drop_table('author_book')
    # ### end Alembic commands ###