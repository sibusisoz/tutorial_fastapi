"""add  cols to  tpost table

Revision ID: ab9214213020
Revises: aa0c0495bb70
Create Date: 2024-08-04 18:26:50.649117

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ab9214213020'
down_revision: Union[str, None] = 'aa0c0495bb70'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table("tusers",sa.Column("id",sa.Integer(),nullable=False)
                    ,sa.Column("email",sa.String(),nullable=False)
                    ,sa.Column("password",sa.String(),nullable=False)
                    ,sa.Column("created_at",sa.TIMESTAMP(timezone=True),server_default=sa.text("now()"),nullable=False)
                    ,sa.PrimaryKeyConstraint("id")
                    ,sa.UniqueConstraint("email"))  
 
    pass


def downgrade() -> None:
    op.drop_table("tusers") 
    pass
