from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, Field


class ItemAdicionalDTO(BaseModel):
    descricao: str
    valor: Decimal


class CriarOrcamentoRequest(BaseModel):
    cliente_id: UUID
    consumo_mensal_kwh: Decimal
    painel_id: UUID
    inversor_id: UUID
    valor_kit: Decimal
    valor_estrutura: Decimal = Decimal("0")
    tipo_estrutura: str = "ceramico"
    custo_deslocamento: Decimal = Decimal("0")
    itens_adicionais: list[ItemAdicionalDTO] = Field(default_factory=list)
    forma_pagamento: str = "avista"  # "avista", "2", "3", "6", "12"


class AtualizarOrcamentoRequest(BaseModel):
    consumo_mensal_kwh: Decimal | None = None
    painel_id: UUID | None = None
    inversor_id: UUID | None = None
    valor_kit: Decimal | None = None
    valor_estrutura: Decimal | None = None
    tipo_estrutura: str | None = None
    custo_deslocamento: Decimal | None = None
    itens_adicionais: list[ItemAdicionalDTO] | None = None
    forma_pagamento: str | None = None


class CalcularMaterialEletricoRequest(BaseModel):
    potencia_inversor_kwp: Decimal


class CalcularMaterialEletricoResponse(BaseModel):
    valor: Decimal


class OrcamentoResponse(BaseModel):
    id: UUID
    tenant_id: UUID
    cliente_id: UUID
    vendedor_id: UUID | None
    status: str

    consumo_mensal_kwh: Decimal
    painel_id: UUID
    painel_modelo: str
    painel_potencia_w: int
    inversor_id: UUID
    inversor_modelo: str
    inversor_potencia_nominal_w: int
    quantidade_paineis: int
    potencia_sistema_kwp: Decimal
    geracao_mensal_kwh: Decimal

    valor_kit: Decimal
    valor_montagem: Decimal
    valor_projeto: Decimal
    valor_estrutura: Decimal
    tipo_estrutura: str
    valor_material_eletrico: Decimal
    custo_deslocamento: Decimal
    itens_adicionais: list[dict]
    valor_itens_adicionais: Decimal
    subtotal: Decimal

    margem_lucro: Decimal
    comissao: Decimal
    imposto: Decimal
    margem_desconto_avista: Decimal

    valor_final: Decimal
    forma_pagamento: str
    taxa_juros: Decimal
    valor_cobrado: Decimal
    numero_parcelas: int
    valor_parcela: Decimal

    model_config = {"from_attributes": True}


class OrcamentoListResponse(BaseModel):
    items: list[OrcamentoResponse]
    total: int
    offset: int
    limit: int
