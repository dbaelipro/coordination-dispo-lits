"""Change libelle varyaing of regions tables

Revision ID: 2821ed848df9
Revises: 98ff6db3b556
Create Date: 2020-04-22 09:41:36.102159

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2821ed848df9'
down_revision = '98ff6db3b556'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('orga_region', 'libelle', existing_type=sa.VARCHAR(length=30))
    # ### end Alembic commands ###


def downgrade():
    op.alter_column('orga_region', 'libelle', existing_type=sa.VARCHAR(length=20))