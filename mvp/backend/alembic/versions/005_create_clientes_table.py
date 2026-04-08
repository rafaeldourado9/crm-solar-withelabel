"""create clientes table

Revision ID: 005
Revises: 004
Create Date: 2024-01-01 00:00:04.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID

# revision identifiers, used by Alembic.
revision: str = '005'
down_revision: Union[str, None] = '004'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'clientes',
        sa.Column('id', UUID(as_uuid=True), primary_key=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.func.now(), nullable=False),
        sa.Column('tenant_id', UUID(as_uuid=True), sa.ForeignKey('tenants.id'), nullable=False),
        sa.Column('vendedor_id', UUID(as_uuid=True), sa.ForeignKey('users.id'), nullable=True),
        sa.Column('nome', sa.String(200), nullable=False),
        sa.Column('cpf_cnpj', sa.String(14), nullable=False),
        sa.Column('telefone', sa.String(20), nullable=False, server_default=''),
        sa.Column('email', sa.String(255), nullable=False, server_default=''),
        sa.Column('endereco', sa.String(300), nullable=False, server_default=''),
        sa.Column('bairro', sa.String(100), nullable=False, server_default=''),
        sa.Column('cidade', sa.String(100), nullable=False, server_default=''),
        sa.Column('estado', sa.String(2), nullable=False, server_default=''),
        sa.Column('cep', sa.String(9), nullable=False, server_default=''),
        sa.Column('status', sa.String(20), nullable=False, server_default='orcamento'),
        sa.Column('ativo', sa.Boolean(), nullable=False, server_default='true'),
    )
    op.create_index('ix_clientes_tenant_id', 'clientes', ['tenant_id'])
    op.create_index('ix_clientes_vendedor_id', 'clientes', ['vendedor_id'])
    op.create_index('ix_clientes_cpf_cnpj', 'clientes', ['cpf_cnpj'])


def downgrade() -> None:
    op.drop_index('ix_clientes_cpf_cnpj', 'clientes')
    op.drop_index('ix_clientes_vendedor_id', 'clientes')
    op.drop_index('ix_clientes_tenant_id', 'clientes')
    op.drop_table('clientes')
