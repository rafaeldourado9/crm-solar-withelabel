"""create templates_docx table

Revision ID: 009
Revises: 008
Create Date: 2024-01-01 00:00:08.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID

revision: str = '009'
down_revision: Union[str, None] = '008'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'templates_docx',
        sa.Column('id', UUID(as_uuid=True), primary_key=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.func.now(), nullable=False),
        sa.Column('tenant_id', UUID(as_uuid=True), sa.ForeignKey('tenants.id'), nullable=False),
        sa.Column('nome', sa.String(200), nullable=False),
        sa.Column('tipo', sa.String(20), nullable=False),
        sa.Column('arquivo_path', sa.String(500), nullable=False),
        sa.Column('tamanho_bytes', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('variaveis_encontradas', sa.JSON(), nullable=False, server_default='[]'),
        sa.Column('ativo', sa.Boolean(), nullable=False, server_default='true'),
    )
    op.create_index('ix_templates_docx_tenant_id', 'templates_docx', ['tenant_id'])
    op.create_index('ix_templates_docx_tipo', 'templates_docx', ['tipo'])


def downgrade() -> None:
    op.drop_index('ix_templates_docx_tipo', 'templates_docx')
    op.drop_index('ix_templates_docx_tenant_id', 'templates_docx')
    op.drop_table('templates_docx')
