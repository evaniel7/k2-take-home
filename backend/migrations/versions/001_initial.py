"""Initial migration - create requests table

Revision ID: 001
Revises:
Create Date: 2024-01-01 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = '001'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create enum type
    request_status = postgresql.ENUM(
        'new', 'accepted', 'deferred', 'declined',
        name='requeststatus'
    )
    request_status.create(op.get_bind())

    op.create_table(
        'requests',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('title', sa.String(255), nullable=False),
        sa.Column('problem_statement', sa.Text(), nullable=False),
        sa.Column('expected_impact', sa.Text(), nullable=False),
        sa.Column('urgency', sa.Integer(), nullable=False),
        sa.Column('status', sa.Enum('new', 'accepted', 'deferred', 'declined', name='requeststatus'), nullable=False, server_default='new'),
        sa.Column('decision_reason', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.func.now()),
    )


def downgrade() -> None:
    op.drop_table('requests')
    op.execute('DROP TYPE requeststatus')
