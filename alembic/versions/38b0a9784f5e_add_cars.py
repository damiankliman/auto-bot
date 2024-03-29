"""Add cars

Revision ID: 38b0a9784f5e
Revises: bfc9f2390ffa
Create Date: 2023-01-04 00:16:24.854367

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
from core.models import CarTypeType

# revision identifiers, used by Alembic.
revision = '38b0a9784f5e'
down_revision = 'bfc9f2390ffa'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    CarTypeType.create(op.get_bind(), checkfirst=True)
    op.create_table('car',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('year', sa.Integer(), nullable=False),
    sa.Column('make', sa.String(), nullable=False),
    sa.Column('model', sa.String(), nullable=False),
    sa.Column('trim', sa.String(), nullable=False),
    sa.Column('type', CarTypeType, nullable=False),
    sa.Column('horsepower', sa.Integer(), nullable=False),
    sa.Column('weight', sa.Integer(), nullable=False),
    sa.Column('price', sa.Integer(), nullable=False),
    sa.Column('order_code', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id'),
    sa.UniqueConstraint('order_code')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('car')
    CarTypeType.drop(op.get_bind(), checkfirst=True)
    # ### end Alembic commands ###
