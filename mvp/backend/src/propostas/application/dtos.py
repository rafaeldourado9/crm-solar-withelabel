from datetime import date
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel


class CriarPropostaRequest(BaseModel):
    orcamento_id: UUID
    data_validade: date
    observacoes: str = ""


class AtualizarPropostaRequest(BaseModel):
    data_validade: date | None = None
    observacoes: str | None = None


class PropostaResponse(BaseModel):
    id: UUID
    tenant_id: UUID
    orcamento_id: UUID
    cliente_id: UUID
    vendedor_id: UUID | None
    numero: str
    status: str
    cliente_nome: str
    cliente_cpf_cnpj: str
    cliente_email: str
    cliente_telefone: str
    cliente_cidade: str
    cliente_estado: str
    potencia_sistema_kwp: Decimal
    quantidade_paineis: int
    painel_modelo: str
    inversor_modelo: str
    geracao_mensal_kwh: Decimal
    valor_final: Decimal
    forma_pagamento: str
    numero_parcelas: int
    valor_parcela: Decimal
    taxa_juros: Decimal
    data_validade: date
    observacoes: str

    model_config = {"from_attributes": True}


class PropostaListResponse(BaseModel):
    items: list[PropostaResponse]
    total: int
    offset: int
    limit: int
