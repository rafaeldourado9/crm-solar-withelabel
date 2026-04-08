"""create propostas table

Revision ID: 007
Revises: 006
Create Date: 2024-01-01 00:00:06.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID

revision: str = '007'
down_revision: Union[str, None] = '006'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'propostas',
        sa.Column('id', UUID(as_uuid=True), primary_key=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.func.now(), nullable=False),
        sa.Column('tenant_id', UUID(as_uuid=True), sa.ForeignKey('tenants.id'), nullable=False),
        sa.Column('orcamento_id', UUID(as_uuid=True), sa.ForeignKey('orcamentos.id'), nullable=False),
        sa.Column('cliente_id', UUID(as_uuid=True), sa.ForeignKey('clientes.id'), nullable=False),
        sa.Column('vendedor_id', UUID(as_uuid=True), sa.ForeignKey('users.id'), nullable=True),
        sa.Column('numero', sa.String(30), nullable=False),
        sa.Column('status', sa.String(20), nullable=False, server_default='pendente'),
        # Snapshot cliente
        sa.Column('cliente_nome', sa.String(200), nullable=False),
        sa.Column('cliente_cpf_cnpj', sa.String(14), nullable=False, server_default=''),
        sa.Column('cliente_email', sa.String(255), nullable=False, server_default=''),
        sa.Column('cliente_telefone', sa.String(20), nullable=False, server_default=''),
        sa.Column('cliente_endereco', sa.String(300), nullable=False, server_default=''),
        sa.Column('cliente_cidade', sa.String(100), nullable=False, server_default=''),
        sa.Column('cliente_estado', sa.String(2), nullable=False, server_default=''),
        sa.Column('cliente_cep', sa.String(9), nullable=False, server_default=''),
        # Dimensionamento
        sa.Column('potencia_sistema_kwp', sa.Numeric(10, 3), nullable=False, server_default='0'),
        sa.Column('quantidade_paineis', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('painel_modelo', sa.String(200), nullable=False, server_default=''),
        sa.Column('inversor_modelo', sa.String(200), nullable=False, server_default=''),
        sa.Column('geracao_mensal_kwh', sa.Numeric(10, 2), nullable=False, server_default='0'),
        # Financeiro
        sa.Column('valor_final', sa.Numeric(12, 2), nullable=False, server_default='0'),
        sa.Column('forma_pagamento', sa.String(10), nullable=False, server_default='avista'),
        sa.Column('numero_parcelas', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('valor_parcela', sa.Numeric(12, 2), nullable=False, server_default='0'),
        sa.Column('taxa_juros', sa.Numeric(5, 2), nullable=False, server_default='0'),
        sa.Column('data_validade', sa.Date(), nullable=False),
        sa.Column('observacoes', sa.String(1000), nullable=False, server_default=''),
    )
    op.create_index('ix_propostas_tenant_id', 'propostas', ['tenant_id'])
    op.create_index('ix_propostas_orcamento_id', 'propostas', ['orcamento_id'])
    op.create_index('ix_propostas_cliente_id', 'propostas', ['cliente_id'])
    op.create_index('ix_propostas_numero', 'propostas', ['numero'])


def downgrade() -> None:
    op.drop_index('ix_propostas_numero', 'propostas')
    op.drop_index('ix_propostas_cliente_id', 'propostas')
    op.drop_index('ix_propostas_orcamento_id', 'propostas')
    op.drop_index('ix_propostas_tenant_id', 'propostas')
    op.drop_table('propostas')
