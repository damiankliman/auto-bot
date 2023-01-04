"""Seed initial cars

Revision ID: 3eb8b2f4634c
Revises: b82fb7a3d204
Create Date: 2023-01-03 21:14:49.039860

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy import table, column
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision = '3eb8b2f4634c'
down_revision = 'b82fb7a3d204'
branch_labels = None
depends_on = None


def upgrade():
    car_table = table(
        "car",
        column("id", postgresql.UUID(as_uuid=True)),
        column("year", sa.Integer),
        column("make", sa.String),
        column("model", sa.String),
        column("trim", sa.String),
        column("type", sa.String),
        column("horsepower", sa.Integer),
        column("weight", sa.Integer),
        column("price", sa.Integer),
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
                "type": "Hatchback",
                "horsepower": 134,
                "weight": 2698,
                "price": 3000,
            },
            {
                "id": "e159a9e5-de67-46a5-b58a-8475045bc946",
                "year": 1994,
                "make": "BMW",
                "model": "318",
                "trim": "i",
                "type": "Coupe",
                "horsepower": 111,
                "weight": 2348,
                "price": 3000,
            },
            {
                "id": "680d3025-a530-45c4-9189-a503bac8c5f7",
                "year": 2003,
                "make": "VW",
                "model": "Golf",
                "trim": "GTI",
                "type": "Hatchback",
                "horsepower": 180,
                "weight": 2674,
                "price": 5000,
            },
            {
                "id": "2bdb326b-d6db-42df-8761-3e28757431e3",
                "year": 1993,
                "make": "Honda",
                "model": "Civic",
                "trim": "Type R",
                "type": "Hatchback",
                "horsepower": 182,
                "weight": 2359,
                "price": 30000,
            },
            {
                "id": "279042cd-e679-4dae-bd80-f0478ecbcc7f",
                "year": 1993,
                "make": "Nissan",
                "model": "Silvia",
                "trim": "Spec R",
                "type": "Coupe",
                "horsepower": 247,
                "weight": 2734,
                "price": 50000,
            },
        ],
    )


def downgrade() -> None:
    pass
