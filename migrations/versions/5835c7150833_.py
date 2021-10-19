"""empty message

Revision ID: 5835c7150833
Revises: 099e10dd71e9
Create Date: 2021-10-06 09:52:40.551440

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '5835c7150833'
down_revision = '099e10dd71e9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('candidate_test_schedule',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('candidate_id', sa.Integer(), nullable=True),
    sa.Column('date_test', sa.DateTime(), nullable=True),
    sa.Column('is_deleted', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['candidate_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('candidate_schedule_test')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('candidate_schedule_test',
    sa.Column('id', mysql.INTEGER(display_width=11), autoincrement=True, nullable=False),
    sa.Column('candidate_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True),
    sa.Column('date_test', mysql.DATETIME(), nullable=True),
    sa.Column('is_deleted', mysql.TINYINT(display_width=1), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['candidate_id'], ['user.id'], name='candidate_schedule_test_ibfk_1'),
    sa.PrimaryKeyConstraint('id'),
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    op.drop_table('candidate_test_schedule')
    # ### end Alembic commands ###
