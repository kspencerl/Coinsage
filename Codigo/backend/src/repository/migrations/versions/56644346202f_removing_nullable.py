"""removing nullable

Revision ID: 56644346202f
Revises: 0a34a0cf0922
Create Date: 2024-04-04 20:30:55.243321

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "56644346202f"
down_revision: Union[str, None] = "0a34a0cf0922"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("analysis", sa.Column("created_at", sa.DateTime(), nullable=False))
    op.add_column("analysis", sa.Column("last_updated", sa.DateTime(), nullable=False))
    op.add_column("analysis_currency_stage_four", sa.Column("created_at", sa.DateTime(), nullable=False))
    op.add_column("analysis_currency_stage_four", sa.Column("last_updated", sa.DateTime(), nullable=False))
    op.add_column("analysis_currency_stage_one", sa.Column("created_at", sa.DateTime(), nullable=False))
    op.add_column("analysis_currency_stage_one", sa.Column("last_updated", sa.DateTime(), nullable=False))
    op.add_column("analysis_currency_stage_three", sa.Column("created_at", sa.DateTime(), nullable=False))
    op.add_column("analysis_currency_stage_three", sa.Column("last_updated", sa.DateTime(), nullable=False))
    op.add_column("analysis_currency_stage_two", sa.Column("created_at", sa.DateTime(), nullable=False))
    op.add_column("analysis_currency_stage_two", sa.Column("last_updated", sa.DateTime(), nullable=False))
    op.add_column("analysis_info_schedule", sa.Column("created_at", sa.DateTime(), nullable=False))
    op.add_column("analysis_info_schedule", sa.Column("last_updated", sa.DateTime(), nullable=False))
    op.add_column("currencies_info_schedule", sa.Column("created_at", sa.DateTime(), nullable=False))
    op.add_column("currencies_info_schedule", sa.Column("last_updated", sa.DateTime(), nullable=False))
    op.add_column("currency_base_info", sa.Column("created_at", sa.DateTime(), nullable=True))
    op.add_column("currency_base_info", sa.Column("last_updated", sa.DateTime(), nullable=True))
    op.add_column("setor", sa.Column("created_at", sa.DateTime(), nullable=False))
    op.add_column("setor", sa.Column("last_updated", sa.DateTime(), nullable=False))
    op.add_column("setor_currency_base_info", sa.Column("created_at", sa.DateTime(), nullable=False))
    op.add_column("setor_currency_base_info", sa.Column("last_updated", sa.DateTime(), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("setor_currency_base_info", "last_updated")
    op.drop_column("setor_currency_base_info", "created_at")
    op.drop_column("setor", "last_updated")
    op.drop_column("setor", "created_at")
    op.drop_column("currency_base_info", "last_updated")
    op.drop_column("currency_base_info", "created_at")
    op.drop_column("currencies_info_schedule", "last_updated")
    op.drop_column("currencies_info_schedule", "created_at")
    op.drop_column("analysis_info_schedule", "last_updated")
    op.drop_column("analysis_info_schedule", "created_at")
    op.drop_column("analysis_currency_stage_two", "last_updated")
    op.drop_column("analysis_currency_stage_two", "created_at")
    op.drop_column("analysis_currency_stage_three", "last_updated")
    op.drop_column("analysis_currency_stage_three", "created_at")
    op.drop_column("analysis_currency_stage_one", "last_updated")
    op.drop_column("analysis_currency_stage_one", "created_at")
    op.drop_column("analysis_currency_stage_four", "last_updated")
    op.drop_column("analysis_currency_stage_four", "created_at")
    op.drop_column("analysis", "last_updated")
    op.drop_column("analysis", "created_at")
    # ### end Alembic commands ###
