"""Add default in booking_date

Revision ID: 1d4de3edbd6d
Revises: e19e6ec83daf
Create Date: 2026-08-10 20:26:21.908777

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = '1d4de3edbd6d'
down_revision: Union[str, Sequence[str], None] = 'e19e6ec83daf'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.alter_column(
        'booking', 
        'booking_date',
        existing_type=postgresql.TIMESTAMP(),
        type_=sa.DateTime(timezone=True),
        server_default=sa.text('CURRENT_TIMESTAMP'),  
        nullable=True,                              
        existing_nullable=False
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.alter_column(
        'booking', 
        'booking_date',
        existing_type=sa.DateTime(timezone=True),
        type_=postgresql.TIMESTAMP(),
        server_default=None,                        
        nullable=False,
        existing_nullable=True
    )