"""Add content column

Revision ID: ccaf7f61fcee
Revises: b7e05598c058
Create Date: 2021-11-29 14:08:00.864167

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ccaf7f61fcee'
down_revision = '4dc437a546c5'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_column('posts','content')
    pass
