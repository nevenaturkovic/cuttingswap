"""Added OfferImage

Revision ID: 6b0481379dda
Revises: 70ca79bd6b4e
Create Date: 2021-11-29 11:35:56.953593

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6b0481379dda'
down_revision = '70ca79bd6b4e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('offer_images',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('mimetype', sa.String(length=6), nullable=False),
    sa.Column('offer_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['offer_id'], ['offers.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('offer_images')
    # ### end Alembic commands ###