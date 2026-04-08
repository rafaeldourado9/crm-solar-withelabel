"""create vendas_vendedor table

Revision ID: 010
Revises: 009
Create Date: 2024-01-01 00:00:09.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID

revision: str = '010'
down_revision: Union[str, None] = '009'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'vendas_vendedor',
        sa.Column('id', UUID(as_uuid=True), primary_key=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.func.now(), nullable=False),
        sa.Column('tenant_id', UUID(as_uuid=True), sa.ForeignKey('tenants.id'), nullable=False),
        sa.Column('contrato_id', UUID(as_uuid=True), sa.ForeignKey('contratos.id'), nullable=False, unique=True),
        sa.Column('vendedor_id', UUID(as_uuid=True), sa.ForeignKey('users.id'), nullable=False),
        sa.Column('valor_venda', sa.Numeric(12, 2), nullable=False),
        sa.Column('valor_comissao', sa.Numeric(12, 2), nullable=False),
        sa.Column('pago', sa.Boolean(), nullable=False, server_default='false'),
    )
    op.create_index('ix_vendas_vendedor_tenant_id', 'vendas_vendedor', ['tenant_id'])
    op.create_index('ix_vendas_vendedor_vendedor_id', 'vendas_vendedor', ['vendedor_id'])
    op.create_index('ix_vendas_vendedor_contrato_id', 'vendas_vendedor', ['contrato_id'])


def downgrade() -> None:
    op.drop_index('ix_vendas_vendedor_contrato_id', 'vendas_vendedor')
    op.drop_index('ix_vendas_vendedor_vendedor_id', 'vendas_vendedor')
    op.drop_index('ix_vendas_vendedor_tenant_id', 'vendas_vendedor')
    op.drop_table('vendas_vendedor')
