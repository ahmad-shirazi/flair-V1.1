"""create document table

Revision ID: 86c8a46064e3
Revises: 
Create Date: 2022-08-13 11:40:54.312553

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '86c8a46064e3'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'document',
        sa.Column('id', sa.BIGINT(), autoincrement=True, primary_key=True),
        sa.Column('fileKey', sa.String(255), nullable=False),
        sa.Column('originalName', sa.String(255), nullable=False),
        sa.Column('originalBucketName', sa.String(255), nullable=False),
        sa.Column('result', sa.String(), nullable=True),
        sa.Column('status', sa.String(255), nullable=True),
        sa.Column('createdAt', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updatedAt', sa.DateTime(timezone=True), nullable=True),
    )
    op.create_index("idx_document_fileKey", "document", ["fileKey"], unique=True)
    op.create_index("idx_document_originalBucketName_originalName", "document", ["originalName", "originalBucketName"],
                    unique=False)


def downgrade():
    op.drop_table('document')
