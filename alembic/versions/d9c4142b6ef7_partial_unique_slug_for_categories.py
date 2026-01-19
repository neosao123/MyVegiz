"""partial unique slug for categories

Revision ID: d9c4142b6ef7
Revises: e8f14c997264
Create Date: 2026-01-19 18:01:28.111403

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd9c4142b6ef7'
down_revision: Union[str, Sequence[str], None] = 'e8f14c997264'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
