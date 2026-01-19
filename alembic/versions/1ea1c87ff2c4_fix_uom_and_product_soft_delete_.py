"""fix uom and product soft delete uniqueness

Revision ID: 1ea1c87ff2c4
Revises: dff6256fcacf
Create Date: 2026-01-19 18:36:07.401180
"""

from typing import Union, Sequence
from alembic import op


# revision identifiers, used by Alembic.
revision: str = '1ea1c87ff2c4'
down_revision: Union[str, Sequence[str], None] = 'dff6256fcacf'
branch_labels = None
depends_on = None


def upgrade() -> None:
    """
    Make uom_short_name and product_short_name unique
    ONLY for non-deleted rows
    """

    # --------------------
    # UOM
    # --------------------
    op.execute("""
        DROP INDEX IF EXISTS ix_uoms_uom_short_name;
    """)

    op.execute("""
        CREATE UNIQUE INDEX ix_uoms_uom_short_name_not_deleted
        ON uoms (uom_short_name)
        WHERE is_delete = false;
    """)

    # --------------------
    # PRODUCT
    # --------------------
    op.execute("""
        DROP INDEX IF EXISTS ix_products_product_short_name;
    """)

    op.execute("""
        CREATE UNIQUE INDEX ix_products_product_short_name_not_deleted
        ON products (product_short_name)
        WHERE is_delete = false;
    """)


def downgrade() -> None:
    """
    Revert back to full unique constraints
    """

    # --------------------
    # UOM
    # --------------------
    op.execute("""
        DROP INDEX IF EXISTS ix_uoms_uom_short_name_not_deleted;
    """)

    op.execute("""
        CREATE UNIQUE INDEX ix_uoms_uom_short_name
        ON uoms (uom_short_name);
    """)

    # --------------------
    # PRODUCT
    # --------------------
    op.execute("""
        DROP INDEX IF EXISTS ix_products_product_short_name_not_deleted;
    """)

    op.execute("""
        CREATE UNIQUE INDEX ix_products_product_short_name
        ON products (product_short_name);
    """)
