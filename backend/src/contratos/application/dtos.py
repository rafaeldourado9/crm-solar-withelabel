from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel


class CriarContratoRequest(BaseModel):
    proposta_id: UUID
    prazo_execucao_dias: int = 30
    garantia_instalacao_meses: int = 12
    foro_comarca: str = ""


class AtualizarContratoRequest(BaseModel):
    prazo_execucao_dias: int | None = None
    garantia_instalacao_meses: int | None = None
    foro_comarca: str | None = None
    status: str | None = None


class ContratoResponse(BaseModel):
    id: UUID
    tenant_id: UUID
    proposta_id: UUID
    cliente_id: UUID
    vendedor_id: UUID | None
    numero: str
    status: str
    cliente_nome: str
    cliente_cpf_cnpj: str
    cliente_cidade: str
    cliente_estado: str
    empresa_razao_social: str
    empresa_cnpj: str
    potencia_total_kwp: Decimal
    quantidade_paineis: int
    valor_total: Decimal
    numero_parcelas: int
    valor_parcela: Decimal
    prazo_execucao_dias: int
    garantia_instalacao_meses: int
    foro_comarca: str

    model_config = {"from_attributes": True}


class ContratoListResponse(BaseModel):
    items: list[ContratoResponse]
    total: int
    offset: int
    limit: int
