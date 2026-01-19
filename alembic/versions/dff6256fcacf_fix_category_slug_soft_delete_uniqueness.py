"""fix category slug soft delete uniqueness

Revision ID: dff6256fcacf
Revises: d9c4142b6ef7
Create Date: 2026-01-19 18:19:27.158812
"""

from typing import Sequence, Union
from alembic import op


# revision identifiers, used by Alembic.
revision: str = 'dff6256fcacf'
down_revision: Union[str, Sequence[str], None] = 'd9c4142b6ef7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """
    Make slug unique ONLY for non-deleted categories
    """

    # 1️⃣ Drop old unique index (if exists)
    op.execute("""
        DROP INDEX IF EXISTS ix_categories_slug;
    """)

    # 2️⃣ Create PARTIAL unique index
    op.execute("""
        CREATE UNIQUE INDEX ix_categories_slug_not_deleted
        ON categories (slug)
        WHERE is_delete = false;
    """)


def downgrade() -> None:
    """
    Revert back to full unique slug (not recommended)
    """

    # Drop partial index
    op.execute("""
        DROP INDEX IF EXISTS ix_categories_slug_not_deleted;
    """)

    # Restore old unique index
    op.execute("""
        CREATE UNIQUE INDEX ix_categories_slug
        ON categories (slug);
    """)
