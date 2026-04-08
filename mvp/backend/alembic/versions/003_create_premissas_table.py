"""create premissas table

Revision ID: 003
Revises: 002
Create Date: 2024-01-01 00:00:02.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID, JSON

# revision identifiers, used by Alembic.
revision: str = '003'
down_revision: Union[str, None] = '002'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'premissas',
        sa.Column('id', UUID(as_uuid=True), primary_key=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.func.now(), nullable=False),
        sa.Column('tenant_id', UUID(as_uuid=True), sa.ForeignKey('tenants.id'), nullable=False),
        sa.Column('ativa', sa.Boolean(), nullable=False, server_default='true'),
        sa.Column('margem_lucro_percentual', sa.Numeric(5, 2), nullable=False, server_default='18'),
        sa.Column('comissao_percentual', sa.Numeric(5, 2), nullable=False, server_default='5'),
        sa.Column('imposto_percentual', sa.Numeric(5, 2), nullable=False, server_default='6'),
        sa.Column('margem_desconto_avista_percentual', sa.Numeric(5, 2), nullable=False, server_default='2'),
        sa.Column('montagem_por_painel', sa.Numeric(10, 2), nullable=False, server_default='70'),
        sa.Column('valor_projeto', sa.Numeric(10, 2), nullable=False, server_default='400'),
        sa.Column('hsp_padrao', sa.Numeric(5, 2), nullable=False, server_default='5.5'),
        sa.Column('perda_padrao', sa.Numeric(5, 4), nullable=False, server_default='0.20'),
        sa.Column('overload_inversor', sa.Numeric(5, 4), nullable=False, server_default='0.70'),
        sa.Column('tarifa_energia_atual', sa.Numeric(10, 2), nullable=False, server_default='0.95'),
        sa.Column('inflacao_energetica_anual', sa.Numeric(5, 4), nullable=False, server_default='0.08'),
        sa.Column('perda_eficiencia_anual', sa.Numeric(5, 4), nullable=False, server_default='0.005'),
        sa.Column('taxas_maquininha', JSON, nullable=False),
        sa.Column('faixas_material_eletrico', JSON, nullable=False),
        sa.Column('consumo_veiculo', sa.Numeric(5, 2), nullable=False, server_default='10'),
        sa.Column('preco_combustivel', sa.Numeric(10, 2), nullable=False, server_default='6.75'),
        sa.Column('margem_deslocamento', sa.Numeric(5, 4), nullable=False, server_default='0.20'),
        sa.Column('cidades_sem_cobranca', JSON, nullable=False),
    )
    op.create_index('ix_premissas_tenant_id', 'premissas', ['tenant_id'])


def downgrade() -> None:
    op.drop_index('ix_premissas_tenant_id', 'premissas')
    op.drop_table('premissas')
