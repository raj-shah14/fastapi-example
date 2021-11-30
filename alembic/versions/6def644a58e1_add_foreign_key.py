"""Add foreign key

Revision ID: 6def644a58e1
Revises: 6c42afdf9ef7
Create Date: 2021-11-29 14:21:19.592196

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6def644a58e1'
down_revision = '6c42afdf9ef7'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('user_id', sa.Integer(), nullable=False))
    op.create_foreign_key('posts_users_fk', source_table="posts", referent_table="users", local_cols=["user_id"], remote_cols=["id"], ondelete="CASCADE")
    pass


def downgrade():
    op.drop_constraint("posts_users_fk", table_name="posts")
    op.drop_column("posts","user_id")
    pass
