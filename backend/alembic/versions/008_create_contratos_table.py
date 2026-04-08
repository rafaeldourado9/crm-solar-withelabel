"""create contratos table

Revision ID: 008
Revises: 007
Create Date: 2024-01-01 00:00:07.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID

revision: str = '008'
down_revision: Union[str, None] = '007'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'contratos',
        sa.Column('id', UUID(as_uuid=True), primary_key=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.func.now(), nullable=False),
        sa.Column('tenant_id', UUID(as_uuid=True), sa.ForeignKey('tenants.id'), nullable=False),
        sa.Column('proposta_id', UUID(as_uuid=True), sa.ForeignKey('propostas.id'), nullable=False, unique=True),
        sa.Column('cliente_id', UUID(as_uuid=True), sa.ForeignKey('clientes.id'), nullable=False),
        sa.Column('vendedor_id', UUID(as_uuid=True), sa.ForeignKey('users.id'), nullable=True),
        sa.Column('numero', sa.String(30), nullable=False),
        sa.Column('status', sa.String(20), nullable=False, server_default='rascunho'),
        # Cliente
        sa.Column('cliente_nome', sa.String(200), nullable=False),
        sa.Column('cliente_cpf_cnpj', sa.String(14), nullable=False, server_default=''),
        sa.Column('cliente_endereco', sa.String(300), nullable=False, server_default=''),
        sa.Column('cliente_bairro', sa.String(100), nullable=False, server_default=''),
        sa.Column('cliente_cidade', sa.String(100), nullable=False, server_default=''),
        sa.Column('cliente_estado', sa.String(2), nullable=False, server_default=''),
        sa.Column('cliente_cep', sa.String(9), nullable=False, server_default=''),
        # Empresa (Tenant)
        sa.Column('empresa_razao_social', sa.String(200), nullable=False),
        sa.Column('empresa_cnpj', sa.String(18), nullable=False, server_default=''),
        sa.Column('empresa_endereco', sa.String(300), nullable=False, server_default=''),
        sa.Column('empresa_cidade', sa.String(100), nullable=False, server_default=''),
        sa.Column('empresa_cep', sa.String(9), nullable=False, server_default=''),
        sa.Column('empresa_representante_nome', sa.String(200), nullable=False, server_default=''),
        sa.Column('empresa_representante_cpf', sa.String(14), nullable=False, server_default=''),
        sa.Column('empresa_representante_rg', sa.String(20), nullable=False, server_default=''),
        # Banco
        sa.Column('banco_nome', sa.String(100), nullable=False, server_default=''),
        sa.Column('banco_agencia', sa.String(20), nullable=False, server_default=''),
        sa.Column('banco_conta', sa.String(30), nullable=False, server_default=''),
        sa.Column('banco_titular', sa.String(200), nullable=False, server_default=''),
        # Valores
        sa.Column('potencia_total_kwp', sa.Numeric(10, 3), nullable=False, server_default='0'),
        sa.Column('quantidade_paineis', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('valor_total', sa.Numeric(12, 2), nullable=False, server_default='0'),
        sa.Column('numero_parcelas', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('valor_parcela', sa.Numeric(12, 2), nullable=False, server_default='0'),
        # Termos
        sa.Column('prazo_execucao_dias', sa.Integer(), nullable=False, server_default='30'),
        sa.Column('garantia_instalacao_meses', sa.Integer(), nullable=False, server_default='12'),
        sa.Column('foro_comarca', sa.String(100), nullable=False, server_default=''),
    )
    op.create_index('ix_contratos_tenant_id', 'contratos', ['tenant_id'])
    op.create_index('ix_contratos_cliente_id', 'contratos', ['cliente_id'])
    op.create_index('ix_contratos_numero', 'contratos', ['numero'])


def downgrade() -> None:
    op.drop_index('ix_contratos_numero', 'contratos')
    op.drop_index('ix_contratos_cliente_id', 'contratos')
    op.drop_index('ix_contratos_tenant_id', 'contratos')
    op.drop_table('contratos')
