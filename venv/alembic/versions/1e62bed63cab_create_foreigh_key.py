"""create foreigh key

Revision ID: 1e62bed63cab
Revises: d80587e60548
Create Date: 2024-08-04 18:59:54.560878

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1e62bed63cab'
down_revision: Union[str, None] = 'ab9214213020'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column ("tposts",sa.Column("owner_id",sa.Integer(),nullable=False))
    op.create_foreign_key("tposts_tusers_fk",source_table="tposts",referent_table="tusers",local_cols=["owner_id"],remote_cols=["id"],ondelete="Cascade")
    pass 

def downgrade() -> None:
    op.drop_column("tposts","owner_id")
    op.drop_constraint("tposts_tusers_fk",table_name="tposts")
    pass
