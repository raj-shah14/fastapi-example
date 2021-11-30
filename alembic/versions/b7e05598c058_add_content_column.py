"""Add content column

Revision ID: b7e05598c058
Revises: 4dc437a546c5
Create Date: 2021-11-29 13:59:56.557714

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql.expression import null


# revision identifiers, used by Alembic.
revision = 'b7e05598c058'
down_revision = '4dc437a546c5'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_column('posts','content')
    pass
