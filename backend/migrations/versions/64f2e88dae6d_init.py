"""
Init

Revision ID: 64f2e88dae6d
Revises:
Create Date: 2025-07-07 10:27:26.513896

"""

from datetime import datetime

from collections.abc import Sequence

# revision identifiers, used by Alembic.
revision: str = "64f2e88dae6d"
down_revision: str | Sequence[str] | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###
