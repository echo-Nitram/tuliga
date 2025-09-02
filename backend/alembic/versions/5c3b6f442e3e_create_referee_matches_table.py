"""create referee_matches table

Revision ID: 5c3b6f442e3e
Revises: bd5ea3c7c478
Create Date: 2025-09-02 16:00:00.000000
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5c3b6f442e3e'
down_revision: Union[str, Sequence[str], None] = 'bd5ea3c7c478'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Create referee_matches table."""
    op.create_table(
        'referee_matches',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('home', sa.String(), nullable=False),
        sa.Column('away', sa.String(), nullable=False),
        sa.Column('date', sa.Date(), nullable=False),
        sa.Column('referee_id', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['referee_id'], ['referees.id'], ondelete='SET NULL'),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index(op.f('ix_referee_matches_id'), 'referee_matches', ['id'], unique=False)


def downgrade() -> None:
    """Drop referee_matches table."""
    op.drop_index(op.f('ix_referee_matches_id'), table_name='referee_matches')
    op.drop_table('referee_matches')
