"""Add channel_op commit

Revision ID: de0628f3c021
Revises: d8dda0b9ad7f
Create Date: 2025-10-20 10:55:30.350734

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'de0628f3c021'
down_revision: Union[str, None] = 'd8dda0b9ad7f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'op',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('chanel_id', sa.String(100), nullable=False),
        sa.Column('invate_url', sa.String, nullable=False),
        sa.Column('join_date', sa.DateTime)
        
    )
    


def downgrade() -> None:
    op.drop_table('op')
