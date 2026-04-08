"""create orcamentos table

Revision ID: 006
Revises: 005
Create Date: 2024-01-01 00:00:05.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID

# revision identifiers, used by Alembic.
revision: str = '006'
down_revision: Union[str, None] = '005'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'orcamentos',
        sa.Column('id', UUID(as_uuid=True), primary_key=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.func.now(), nullable=False),
        sa.Column('tenant_id', UUID(as_uuid=True), sa.ForeignKey('tenants.id'), nullable=False),
        sa.Column('cliente_id', UUID(as_uuid=True), sa.ForeignKey('clientes.id'), nullable=False),
        sa.Column('vendedor_id', UUID(as_uuid=True), sa.ForeignKey('users.id'), nullable=True),
        sa.Column('status', sa.String(20), nullable=False, server_default='rascunho'),

        # Dimensionamento
        sa.Column('consumo_mensal_kwh', sa.Numeric(10, 2), nullable=False),
        sa.Column('painel_id', UUID(as_uuid=True), nullable=False),
        sa.Column('painel_modelo', sa.String(200), nullable=False, server_default=''),
        sa.Column('painel_potencia_w', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('inversor_id', UUID(as_uuid=True), nullable=False),
        sa.Column('inversor_modelo', sa.String(200), nullable=False, server_default=''),
        sa.Column('inversor_potencia_nominal_w', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('quantidade_paineis', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('potencia_sistema_kwp', sa.Numeric(10, 3), nullable=False, server_default='0'),
        sa.Column('geracao_mensal_kwh', sa.Numeric(10, 2), nullable=False, server_default='0'),

        # Custos
        sa.Column('valor_kit', sa.Numeric(12, 2), nullable=False, server_default='0'),
        sa.Column('valor_montagem', sa.Numeric(10, 2), nullable=False, server_default='0'),
        sa.Column('valor_projeto', sa.Numeric(10, 2), nullable=False, server_default='0'),
        sa.Column('valor_estrutura', sa.Numeric(10, 2), nullable=False, server_default='0'),
        sa.Column('tipo_estrutura', sa.String(30), nullable=False, server_default='ceramico'),
        sa.Column('valor_material_eletrico', sa.Numeric(10, 2), nullable=False, server_default='0'),
        sa.Column('custo_deslocamento', sa.Numeric(10, 2), nullable=False, server_default='0'),
        sa.Column('itens_adicionais', sa.JSON(), nullable=False, server_default='[]'),
        sa.Column('valor_itens_adicionais', sa.Numeric(10, 2), nullable=False, server_default='0'),
        sa.Column('subtotal', sa.Numeric(12, 2), nullable=False, server_default='0'),

        # Margens
        sa.Column('margem_lucro', sa.Numeric(5, 2), nullable=False, server_default='18'),
        sa.Column('comissao', sa.Numeric(5, 2), nullable=False, server_default='5'),
        sa.Column('imposto', sa.Numeric(5, 2), nullable=False, server_default='6'),
        sa.Column('margem_desconto_avista', sa.Numeric(5, 2), nullable=False, server_default='2'),

        # Valores finais
        sa.Column('valor_final', sa.Numeric(12, 2), nullable=False, server_default='0'),
        sa.Column('forma_pagamento', sa.String(10), nullable=False, server_default='avista'),
        sa.Column('taxa_juros', sa.Numeric(5, 2), nullable=False, server_default='0'),
        sa.Column('valor_cobrado', sa.Numeric(12, 2), nullable=False, server_default='0'),
        sa.Column('numero_parcelas', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('valor_parcela', sa.Numeric(12, 2), nullable=False, server_default='0'),

        # Economia
        sa.Column('economia_25_anos', sa.JSON(), nullable=False, server_default='[]'),
    )
    op.create_index('ix_orcamentos_tenant_id', 'orcamentos', ['tenant_id'])
    op.create_index('ix_orcamentos_cliente_id', 'orcamentos', ['cliente_id'])
    op.create_index('ix_orcamentos_vendedor_id', 'orcamentos', ['vendedor_id'])


def downgrade() -> None:
    op.drop_index('ix_orcamentos_vendedor_id', 'orcamentos')
    op.drop_index('ix_orcamentos_cliente_id', 'orcamentos')
    op.drop_index('ix_orcamentos_tenant_id', 'orcamentos')
    op.drop_table('orcamentos')
