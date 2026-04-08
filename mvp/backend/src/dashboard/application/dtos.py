from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel


class TopVendedor(BaseModel):
    vendedor_id: UUID
    nome: str
    total_contratos: int
    valor_total: Decimal


class UltimoCliente(BaseModel):
    id: UUID
    nome: str
    telefone: str
    status: str
    created_at: str


class DashboardResponse(BaseModel):
    total_clientes: int
    leads_30d: int
    propostas_ativas: int
    contratos_mes: int
    faturamento_mensal: Decimal
    comissoes_pendentes: Decimal
    top_vendedores: list[TopVendedor]
    ultimos_clientes: list[UltimoCliente]
