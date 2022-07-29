"""005_add_invitation_status

Revision ID: 005_add_invitation_status
Revises: 004_add_field_creator_id
Create Date: 2022-07-27 21:07:36.314954

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
from sqlalchemy.dialects.mysql import ENUM

from core.models.user_event import Status

revision = '005_add_invitation_status'
down_revision = '004_add_field_creator_id'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # enum_type = postgresql.ENUM(Status, values_callable=lambda enum: [e.value for e in enum])
    op.add_column(
        'user_event',
        sa.Column('status', sa.Enum('DECLINED', 'PENDING', 'ACCEPTED', name='status'), nullable=True)
    )

def downgrade() -> None:
    op.drop_column('user_event', 'status')
