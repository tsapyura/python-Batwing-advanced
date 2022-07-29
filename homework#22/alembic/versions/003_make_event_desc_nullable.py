"""003_make_event_desc_nullable

Revision ID: 62c876306a74
Revises: 002_add_event_relation
Create Date: 2022-07-22 11:55:21.465339

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '003_make_event_desc_nullable'
down_revision = '002_add_event_relation'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.alter_column('event', 'description', nullable=True)


def downgrade() -> None:
    op.drop_column('event', 'description', nullable=False)
