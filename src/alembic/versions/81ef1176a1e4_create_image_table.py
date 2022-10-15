"""create image table

Revision ID: 81ef1176a1e4
Revises: 86c8a46064e3
Create Date: 2022-08-13 11:41:04.138308

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '81ef1176a1e4'
down_revision = '86c8a46064e3'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'image',
        sa.Column('id', sa.BIGINT(), autoincrement=True, primary_key=True),
        sa.Column('fileKey', sa.String(255), nullable=False),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('bucketName', sa.String(255), nullable=False),
        sa.Column('number', sa.INT(), nullable=False, default=1),
        sa.Column('noiseRemovedName', sa.String(255), nullable=True),
        sa.Column('noiseRemovedBucketName', sa.String(255), nullable=True),
        sa.Column('ocrName', sa.String(255), nullable=True),
        sa.Column('ocrBucketName', sa.String(255), nullable=True),
        sa.Column('result', sa.String(), nullable=True),
        sa.Column('status', sa.String(255), nullable=True),
        sa.Column('createdAt', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updatedAt', sa.DateTime(timezone=True), nullable=True),
    )
    op.create_index("idx_image_fileKey", "image", ["fileKey"], unique=False)
    op.create_index("idx_image_name_bucketName", "image", ["name", "bucketName"], unique=False)
    op.create_index("idx_image_noiseRemovedName_noiseRemovedBucketName",
                    "image", ["noiseRemovedName", "noiseRemovedBucketName"], unique=False)
    op.create_index("idx_image_ocrName_ocrBucketName",
                    "image", ["ocrName", "ocrBucketName"], unique=False)


def downgrade():
    op.drop_table('image')
