"""Added employee_id and designation

Revision ID: 7e2c508ea49a
Revises: be36048a0c77
Create Date: 2026-07-24 23:26:52.247060
"""

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "7e2c508ea49a"
down_revision = "be36048a0c77"
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table("users") as batch_op:
        batch_op.add_column(
            sa.Column("employee_id", sa.String(length=20), nullable=True)
        )

        batch_op.add_column(
            sa.Column("designation", sa.String(length=100), nullable=True)
        )

        batch_op.create_unique_constraint(
            "uq_users_employee_id",
            ["employee_id"]
        )


def downgrade():
    with op.batch_alter_table("users") as batch_op:
        batch_op.drop_constraint(
            "uq_users_employee_id",
            type_="unique"
        )

        batch_op.drop_column("designation")
        batch_op.drop_column("employee_id")