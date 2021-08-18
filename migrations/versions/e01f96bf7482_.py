"""empty message

Revision ID: e01f96bf7482
Revises: 45187e70a237
Create Date: 2021-08-16 11:32:47.843192

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e01f96bf7482'
down_revision = '45187e70a237'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('candidate_schedule_test_ibfk_1', 'candidate_schedule_test', type_='foreignkey')
    op.create_foreign_key(None, 'candidate_schedule_test', 'user', ['candidate_id'], ['id'])
    op.drop_constraint('candidate_test_ibfk_1', 'candidate_test', type_='foreignkey')
    op.create_foreign_key(None, 'candidate_test', 'user', ['candidate_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'candidate_test', type_='foreignkey')
    op.create_foreign_key('candidate_test_ibfk_1', 'candidate_test', 'candidate', ['candidate_id'], ['id'])
    op.drop_constraint(None, 'candidate_schedule_test', type_='foreignkey')
    op.create_foreign_key('candidate_schedule_test_ibfk_1', 'candidate_schedule_test', 'candidate', ['candidate_id'], ['id'])
    # ### end Alembic commands ###
