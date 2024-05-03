"""Add content column to posts table

Revision ID: ad1f3549966e
Revises: d2e94434a9f6
Create Date: 2024-05-03 14:02:22.012186

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ad1f3549966e'
down_revision: Union[str, None] = 'd2e94434a9f6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass
