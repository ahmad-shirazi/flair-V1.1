"""create token table

Revision ID: b2a4771c7c29
Revises: 81ef1176a1e4
Create Date: 2022-08-22 18:49:26.106971

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b2a4771c7c29'
down_revision = '81ef1176a1e4'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'token',
        sa.Column('id', sa.BIGINT(), autoincrement=True, primary_key=True),
        sa.Column('fileKey', sa.String(255), nullable=False),
        sa.Column('key', sa.String(), nullable=True),
        sa.Column('value', sa.String(255), nullable=True),
        sa.Column('createdAt', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updatedAt', sa.DateTime(timezone=True), nullable=True),
    )
    op.create_index("idx_tokens_fileKey", "token", ["fileKey"], unique=False)


def downgrade():
    op.drop_table('token')
