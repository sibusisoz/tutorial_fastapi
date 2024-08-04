"""create tpost table

Revision ID: 1484394f7de2
Revises: 
Create Date: 2024-08-04 18:05:21.602858

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1484394f7de2'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table("tposts",sa.Column("id",sa.Integer(),nullable=False,primary_key=True)
                    ,sa.Column("title",sa.String(),nullable=False))
    pass


def downgrade() -> None:
    op.drop_table("tposts")
    pass
