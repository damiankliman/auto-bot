"""Seen initial mods

Revision ID: 34183002396a
Revises: e2d21b5f5ac0
Create Date: 2023-01-08 21:04:29.807170

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy import table, column
from sqlalchemy.dialects import postgresql
from core.models import ModTypeType


# revision identifiers, used by Alembic.
revision = '34183002396a'
down_revision = 'e2d21b5f5ac0'
branch_labels = None
depends_on = None


def upgrade() -> None:
    mod_table = table(
        "mod",
        column("id", postgresql.UUID(as_uuid=True)),
        column("name", sa.String),
        column("type", ModTypeType),
        column("price", sa.Integer),
        column("power_add", sa.Integer),
        column("order_code", sa.String),
    )

    op.bulk_insert(
        mod_table,
        [
            {
                "id": "1df628bb-38ed-4c53-b142-77311dbe43f4",
                "name": "T28 turbo kit",
                "type": "INDUCTION",
                "price": 2100,
                "power_add": 100,
                "order_code": "TK1"
            },
            {
                "id": "85633ae7-13bb-4e76-afbd-9c6760ca55b1",
                "name": "Ebay intercooler kit",
                "type": "INTERCOOLER",
                "price": 1000,
                "power_add": 40,
                "order_code": "FM1"
            },
            {
                "id": "01ea0ba0-f33d-48e2-b412-faffac072c85",
                "name": "Pod filter",
                "type": "INTAKE",
                "price": 300,
                "power_add": 10,
                "order_code": "PF1"
            },
            {
                "id": "269c2878-d665-4796-86b0-3fb7f3bea1c3",
                "name": "Ebay cannon exhaust",
                "type": "EXHAUST",
                "price": 700,
                "power_add": 20,
                "order_code": "EX1"
            },
        ]
    )

    pass


def downgrade() -> None:
    pass
