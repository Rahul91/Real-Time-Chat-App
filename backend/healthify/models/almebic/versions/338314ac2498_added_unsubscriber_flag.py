"""Added unsubscriber flag

Revision ID: 338314ac2498
Revises: c7ec268c1001
Create Date: 2016-07-19 17:05:22.965573

"""

# revision identifiers, used by Alembic.
revision = '338314ac2498'
down_revision = 'c7ec268c1001'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user_channel_mapping', sa.Column('is_unsubscribed', mysql.TINYINT(display_width=1), nullable=False))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user_channel_mapping', 'is_unsubscribed')
    ### end Alembic commands ###
