"""empty message

Revision ID: 7db8766e5cf4
Revises: 50fcdc8aa6a3
Create Date: 2021-09-08 17:24:34.586871

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '7db8766e5cf4'
down_revision = '50fcdc8aa6a3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('psikotest', sa.Column('test_filename', sa.String(length=128), nullable=True))
    op.add_column('psikotest', sa.Column('instruction_filename', sa.String(length=128), nullable=True))
    op.drop_column('psikotest', 'instruction')
    op.drop_column('psikotest', 'filename')
    op.add_column('psikotest_type', sa.Column('preliminary', sa.Text(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('psikotest_type', 'preliminary')
    op.add_column('psikotest', sa.Column('filename', mysql.VARCHAR(length=128), nullable=True))
    op.add_column('psikotest', sa.Column('instruction', mysql.TEXT(), nullable=True))
    op.drop_column('psikotest', 'instruction_filename')
    op.drop_column('psikotest', 'test_filename')
    # ### end Alembic commands ###
