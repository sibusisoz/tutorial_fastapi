"""add more cols post

Revision ID: f9979991e4b9
Revises: 1e62bed63cab
Create Date: 2024-08-04 19:28:11.628809

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f9979991e4b9'
down_revision: Union[str, None] = '1e62bed63cab'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
            
    op.add_column ("tposts",sa.Column("published",sa.Boolean(),server_default=("TRUE"),nullable=False),)
    op.add_column ("tposts",sa.Column("created_at",sa.TIMESTAMP(timezone=True),server_default=sa.text("now()"),nullable=False),)
    pass


def downgrade() -> None:
    op.drop_column("tposts","published")
    op.drop_column("tposts","created_at")
    pass
