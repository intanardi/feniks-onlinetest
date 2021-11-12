"""empty message

Revision ID: 099e10dd71e9
Revises: 
Create Date: 2021-10-06 09:51:21.452114

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '099e10dd71e9'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('candidate_test')
    op.drop_table('division_test')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('division_test',
    sa.Column('id', mysql.INTEGER(display_width=11), autoincrement=True, nullable=False),
    sa.Column('filename', mysql.VARCHAR(length=128), nullable=True),
    sa.Column('instruction', mysql.TEXT(), nullable=True),
    sa.Column('examination_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True),
    sa.Column('is_deleted', mysql.TINYINT(display_width=1), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['examination_id'], ['examination.id'], name='division_test_ibfk_1'),
    sa.PrimaryKeyConstraint('id'),
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    op.create_table('candidate_test',
    sa.Column('id', mysql.INTEGER(display_width=11), autoincrement=True, nullable=False),
    sa.Column('candidate_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True),
    sa.Column('psikotest_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True),
    sa.Column('division_test_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True),
    sa.Column('is_deleted', mysql.TINYINT(display_width=1), autoincrement=False, nullable=True),
    sa.Column('status', mysql.TINYINT(display_width=1), autoincrement=False, nullable=True),
    sa.Column('flag', mysql.TINYINT(display_width=1), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['candidate_id'], ['user.id'], name='candidate_test_ibfk_1'),
    sa.ForeignKeyConstraint(['division_test_id'], ['division_test.id'], name='candidate_test_ibfk_2'),
    sa.ForeignKeyConstraint(['psikotest_id'], ['psikotest.id'], name='candidate_test_ibfk_3'),
    sa.PrimaryKeyConstraint('id'),
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    # ### end Alembic commands ###