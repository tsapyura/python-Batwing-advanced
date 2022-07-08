"""002_create_books

Revision ID: 8dc37946f0d2
Revises: 001_create_authors
Create Date: 2022-07-08 13:35:53.529769

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '002_create_books'
down_revision = '001_create_authors'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "books",
        sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("name_of_book", sa.String(255), nullable=False, unique=True))


def downgrade() -> None:
    op.drop_table('books')

