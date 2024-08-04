"""cadd  cols to  tpost table

Revision ID: aa0c0495bb70
Revises: 1484394f7de2
Create Date: 2024-08-04 18:18:40.115642

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'aa0c0495bb70'
down_revision: Union[str, None] = '1484394f7de2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column ("tposts",sa.Column("content",sa.String(),nullable=False))
    pass


def downgrade() -> None:
    op.drop_column("tposts","content")
    pass
