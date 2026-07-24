"""Add assigned_at to complaints

Revision ID: 704cad2886b1
Revises: 82844f1fe74f
Create Date: 2026-07-21 10:27:31.099406
"""

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "704cad2886b1"
down_revision = "82844f1fe74f"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        "complaints",
        sa.Column("assigned_at", sa.DateTime(), nullable=True)
    )


def downgrade():
    op.drop_column("complaints", "assigned_at")