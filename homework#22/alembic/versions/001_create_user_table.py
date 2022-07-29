"""001_create_user_table
Revision ID: 001_create_user_table
Revises: 
Create Date: 2022-07-22 13:36:17.794464
"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '001_create_user_table'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "user",
        sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("email", sa.String(350), unique=True, nullable=False),
        sa.Column("name", sa.String(100), nullable=False),
        sa.Column("password", sa.String, nullable=False),
    )


def downgrade() -> None:
    op.drop_table("user")
