"""Create schema

Revision ID: 1
Revises:
Create Date: 2024-08-16 07:16:14.840299+00:00
"""
from alembic import op

# revision identifiers, used by Alembic.
revision = '1'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.execute("CREATE SCHEMA IF NOT EXISTS common")
    op.execute("CREATE SCHEMA IF NOT EXISTS data")
    op.execute("CREATE SCHEMA IF NOT EXISTS logs")


def downgrade():
    op.execute("DROP SCHEMA IF EXISTS common")
    op.execute("DROP SCHEMA IF EXISTS data")
    op.execute("DROP SCHEMA IF EXISTS logs")

    op.execute("DROP TYPE IF EXISTS value_data_type")
    op.execute("DROP TYPE IF EXISTS html_document_type")
    op.execute("DROP TYPE IF EXISTS content_type")
