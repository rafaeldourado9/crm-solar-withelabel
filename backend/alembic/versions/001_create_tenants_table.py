"""create tenants table

Revision ID: 001
Revises: 
Create Date: 2024-01-01 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID

# revision identifiers, used by Alembic.
revision: str = '001'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'tenants',
        sa.Column('id', UUID(as_uuid=True), primary_key=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.func.now(), nullable=False),
        sa.Column('nome_fantasia', sa.String(200), nullable=False),
        sa.Column('razao_social', sa.String(200), nullable=False),
        sa.Column('cnpj', sa.String(18), nullable=False, unique=True),
        sa.Column('endereco', sa.String(300), nullable=False),
        sa.Column('cidade', sa.String(100), nullable=False),
        sa.Column('estado', sa.String(2), nullable=False),
        sa.Column('cep', sa.String(9), nullable=False),
        sa.Column('representante_nome', sa.String(200), nullable=False),
        sa.Column('representante_cpf', sa.String(14), nullable=False),
        sa.Column('representante_rg', sa.String(20), nullable=False, server_default=''),
        sa.Column('banco_nome', sa.String(100), nullable=False, server_default=''),
        sa.Column('banco_agencia', sa.String(10), nullable=False, server_default=''),
        sa.Column('banco_conta', sa.String(20), nullable=False, server_default=''),
        sa.Column('banco_titular', sa.String(200), nullable=False, server_default=''),
        sa.Column('logo_url', sa.String(500), nullable=True),
        sa.Column('cor_primaria', sa.String(7), nullable=False, server_default='#1E40AF'),
        sa.Column('cor_secundaria', sa.String(7), nullable=False, server_default='#F59E0B'),
        sa.Column('dominio_customizado', sa.String(200), nullable=True),
        sa.Column('plano', sa.String(20), nullable=False, server_default='free'),
        sa.Column('ativo', sa.Boolean(), nullable=False, server_default='true'),
    )
    op.create_index('ix_tenants_cnpj', 'tenants', ['cnpj'])


def downgrade() -> None:
    op.drop_index('ix_tenants_cnpj', 'tenants')
    op.drop_table('tenants')
