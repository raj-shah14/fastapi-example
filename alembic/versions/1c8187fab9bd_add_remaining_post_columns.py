"""Add remaining post columns

Revision ID: 1c8187fab9bd
Revises: 6def644a58e1
Create Date: 2021-11-29 14:27:50.685520

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1c8187fab9bd'
down_revision = '6def644a58e1'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('published', sa.Boolean, server_default="TRUE", nullable=False))
    op.add_column('posts', sa.Column("created_at", sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False))
    pass


def downgrade():
    op.drop_column('posts','published')
    op.drop_column('posts', "created_at")
    pass
