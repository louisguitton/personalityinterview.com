"""submissions

Revision ID: 66b5da6e431d
Revises: eabae6939f55
Create Date: 2018-06-26 10:59:05.257066

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '66b5da6e431d'
down_revision = 'eabae6939f55'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('submission',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=True),
        sa.Column('creation_date', sa.DateTime(), nullable=True),
        sa.Column('submission_date', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_submission_creation_date'), 'submission', ['creation_date'], unique=False)
    op.create_index(op.f('ix_submission_submission_date'), 'submission', ['submission_date'], unique=False)
    op.create_table('submission_questions',
        sa.Column('submission_id', sa.Integer(), nullable=True),
        sa.Column('question_id', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['question_id'], ['question.id'], ),
        sa.ForeignKeyConstraint(['submission_id'], ['submission.id'], )
    )

    with op.batch_alter_table('video') as bop:
        bop.add_column(sa.Column('submission_id', sa.Integer(), nullable=True))
        bop.create_foreign_key('fk_video_submission', 'submission', ['submission_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('video') as bop:
        bop.drop_column('submission_id')
    op.drop_table('submission_questions')
    op.drop_table('submission')
    # ### end Alembic commands ###
