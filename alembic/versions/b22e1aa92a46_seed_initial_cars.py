"""Seed initial cars

Revision ID: b22e1aa92a46
Revises: 38b0a9784f5e
Create Date: 2023-01-04 00:36:48.079076

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy import table, column
from sqlalchemy.dialects import postgresql
from core.models import CarTypeType


# revision identifiers, used by Alembic.
revision = 'b22e1aa92a46'
down_revision = '38b0a9784f5e'
branch_labels = None
depends_on = None


def upgrade() -> None:
    car_table = table(
        "car",
        column("id", postgresql.UUID(as_uuid=True)),
        column("year", sa.Integer),
        column("make", sa.String),
        column("model", sa.String),
        column("trim", sa.String),
        column("type", CarTypeType),
        column("horsepower", sa.Integer),
        column("weight", sa.Integer),
        column("price", sa.Integer),
        column("order_code", sa.String),
    )

    op.bulk_insert(
        car_table,
        [
            {
                "id": "0c1c54f3-9382-42b8-949b-69c5af49f8d4",
                "year": 1993,
                "make": "Nissan",
                "model": "240sx",
                "trim": "SE",
                "type": "HATCHBACK",
                "horsepower": 134,
                "weight": 2698,
                "price": 3000,
                "order_code": "S13A",
            },
            {
                "id": "e159a9e5-de67-46a5-b58a-8475045bc946",
                "year": 1994,
                "make": "BMW",
                "model": "318",
                "trim": "i",
                "type": "COUPE",
                "horsepower": 111,
                "weight": 2348,
                "price": 3000,
                "order_code": "E36A",
            },
            {
                "id": "680d3025-a530-45c4-9189-a503bac8c5f7",
                "year": 2003,
                "make": "VW",
                "model": "Golf",
                "trim": "GTI",
                "type": "HATCHBACK",
                "horsepower": 180,
                "weight": 2674,
                "price": 5000,
                "order_code": "MK4A",
            },
            {
                "id": "2bdb326b-d6db-42df-8761-3e28757431e3",
                "year": 1993,
                "make": "Honda",
                "model": "Civic",
                "trim": "Type R",
                "type": "HATCHBACK",
                "horsepower": 182,
                "weight": 2359,
                "price": 30000,
                "order_code": "EK9A",
            },
            {
                "id": "279042cd-e679-4dae-bd80-f0478ecbcc7f",
                "year": 1993,
                "make": "Nissan",
                "model": "Silvia",
                "trim": "Spec R",
                "type": "COUPE",
                "horsepower": 247,
                "weight": 2734,
                "price": 50000,
                "order_code": "S15A",
            },
        ],
    )


def downgrade() -> None:
    pass
