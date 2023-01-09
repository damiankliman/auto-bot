"""Add factory induction cars

Revision ID: bdd82a0483cf
Revises: 34183002396a
Create Date: 2023-01-08 22:05:43.605894

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bdd82a0483cf'
down_revision = '34183002396a'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('car', sa.Column('factory_induction', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('car', 'factory_induction')
    # ### end Alembic commands ###
