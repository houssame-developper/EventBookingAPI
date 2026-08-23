"""merge heads

Revision ID: 911a50a1c9cc
Revises: 1d4de3edbd6d, 86078545cd66
Create Date: 2026-08-22 20:01:10.266095

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = '911a50a1c9cc'
down_revision: Union[str, Sequence[str], None] = ('1d4de3edbd6d', '86078545cd66')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
