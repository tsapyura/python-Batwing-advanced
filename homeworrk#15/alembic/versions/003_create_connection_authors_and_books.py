"""003_create_connection_authors_and_books

Revision ID: 07f997100d38
Revises: 002_create_books
Create Date: 2022-07-08 13:46:51.465126

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '003_create_author_title_table'
down_revision = '002_create_books'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "author_and_book",
        sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("author", sa.String, nullable=False),
        sa.Column("name_of_book", sa.String, nullable=False))


def downgrade() -> None:
    op.drop_table('author_and_book')
