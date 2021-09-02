"""empty message

Revision ID: 61a4b849e911
Revises: 3956301b8aae
Create Date: 2021-09-02 10:19:51.907851

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '61a4b849e911'
down_revision = '3956301b8aae'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('division', sa.Column('is_deleted', sa.Boolean(), nullable=True))
    op.drop_column('division', 'status')
    op.add_column('examination', sa.Column('is_deleted', sa.Boolean(), nullable=True))
    op.drop_column('examination', 'status')
    op.add_column('level', sa.Column('is_deleted', sa.Boolean(), nullable=True))
    op.drop_column('level', 'status')
    op.add_column('multiple_choice', sa.Column('is_deleted', sa.Boolean(), nullable=True))
    op.drop_column('multiple_choice', 'status')
    op.add_column('psikotest', sa.Column('is_deleted', sa.Boolean(), nullable=True))
    op.drop_column('psikotest', 'status')
    op.add_column('psikotest_type', sa.Column('is_deleted', sa.Boolean(), nullable=True))
    op.drop_column('psikotest_type', 'status')
    op.add_column('question', sa.Column('is_deleted', sa.Boolean(), nullable=True))
    op.drop_column('question', 'status')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('question', sa.Column('status', mysql.TINYINT(display_width=1), autoincrement=False, nullable=True))
    op.drop_column('question', 'is_deleted')
    op.add_column('psikotest_type', sa.Column('status', mysql.TINYINT(display_width=1), autoincrement=False, nullable=True))
    op.drop_column('psikotest_type', 'is_deleted')
    op.add_column('psikotest', sa.Column('status', mysql.TINYINT(display_width=1), autoincrement=False, nullable=True))
    op.drop_column('psikotest', 'is_deleted')
    op.add_column('multiple_choice', sa.Column('status', mysql.TINYINT(display_width=1), autoincrement=False, nullable=True))
    op.drop_column('multiple_choice', 'is_deleted')
    op.add_column('level', sa.Column('status', mysql.TINYINT(display_width=1), autoincrement=False, nullable=True))
    op.drop_column('level', 'is_deleted')
    op.add_column('examination', sa.Column('status', mysql.TINYINT(display_width=1), autoincrement=False, nullable=True))
    op.drop_column('examination', 'is_deleted')
    op.add_column('division', sa.Column('status', mysql.TINYINT(display_width=1), autoincrement=False, nullable=True))
    op.drop_column('division', 'is_deleted')
    # ### end Alembic commands ###
