"""004_add_field_creator_id

Revision ID: 004_add_field_creator_id
Revises: 003_make_event_desc_nullable
Create Date: 2022-07-27 18:45:54.076665

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '004_add_field_creator_id'
down_revision = '003_make_event_desc_nullable'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        'event',
        sa.Column('creator_id', sa.Integer(), nullable=False)
        )


def downgrade() -> None:
    op.drop_column('event', 'creator_id')
