"""create paineis and inversores tables

Revision ID: 004
Revises: 003
Create Date: 2024-01-01 00:00:03.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID

# revision identifiers, used by Alembic.
revision: str = '004'
down_revision: Union[str, None] = '003'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Paineis
    op.create_table(
        'paineis',
        sa.Column('id', UUID(as_uuid=True), primary_key=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.func.now(), nullable=False),
        sa.Column('tenant_id', UUID(as_uuid=True), sa.ForeignKey('tenants.id'), nullable=False),
        sa.Column('modelo', sa.String(200), nullable=False),
        sa.Column('fabricante', sa.String(200), nullable=False),
        sa.Column('potencia_w', sa.Integer(), nullable=False),
        sa.Column('eficiencia', sa.Numeric(5, 2), nullable=False),
        sa.Column('garantia_anos', sa.Integer(), nullable=False, server_default='25'),
        sa.Column('preco', sa.Numeric(10, 2), nullable=False),
        sa.Column('ativo', sa.Boolean(), nullable=False, server_default='true'),
    )
    op.create_index('ix_paineis_tenant_id', 'paineis', ['tenant_id'])

    # Inversores
    op.create_table(
        'inversores',
        sa.Column('id', UUID(as_uuid=True), primary_key=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.func.now(), nullable=False),
        sa.Column('tenant_id', UUID(as_uuid=True), sa.ForeignKey('tenants.id'), nullable=False),
        sa.Column('modelo', sa.String(200), nullable=False),
        sa.Column('fabricante', sa.String(200), nullable=False),
        sa.Column('potencia_nominal_w', sa.Integer(), nullable=False),
        sa.Column('potencia_maxima_w', sa.Integer(), nullable=False),
        sa.Column('eficiencia', sa.Numeric(5, 2), nullable=False),
        sa.Column('garantia_anos', sa.Integer(), nullable=False, server_default='10'),
        sa.Column('preco', sa.Numeric(10, 2), nullable=False),
        sa.Column('ativo', sa.Boolean(), nullable=False, server_default='true'),
    )
    op.create_index('ix_inversores_tenant_id', 'inversores', ['tenant_id'])


def downgrade() -> None:
    op.drop_index('ix_inversores_tenant_id', 'inversores')
    op.drop_table('inversores')
    op.drop_index('ix_paineis_tenant_id', 'paineis')
    op.drop_table('paineis')
