"""Add user__prem commit

Revision ID: d8dda0b9ad7f
Revises: 
Create Date: 2024-02-08 11:55:03.559227

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd8dda0b9ad7f'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('users', sa.Column('premium', sa.Boolean, default=False))


def downgrade() -> None:
    op.drop_column('users', 'premium')
