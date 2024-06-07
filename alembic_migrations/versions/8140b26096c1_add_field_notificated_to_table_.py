"""add field notificated to table notification

Revision ID: 8140b26096c1
Revises: 0afaebc7111d
Create Date: 2024-06-07 15:50:35.065482

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8140b26096c1'
down_revision: Union[str, None] = '0afaebc7111d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('notification', sa.Column('notificated', sa.Boolean(), nullable=False, server_default=sa.false()))
    # ### end Alembic commands ###
    op.alter_column('notification', 'notificated', server_default=None)


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('notification', 'notificated')
    # ### end Alembic commands ###
