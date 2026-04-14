from datetime import date, datetime, timezone
from decimal import Decimal
from enum import Enum
from uuid import UUID

from src.shared.base_entity import TenantEntity


class StatusProposta(str, Enum):
    PENDENTE = "pendente"
    ACEITA = "aceita"
    RECUSADA = "recusada"


class Proposta(TenantEntity):
    orcamento_id: UUID
    cliente_id: UUID
    vendedor_id: UUID | None = None
    numero: str

    status: StatusProposta = StatusProposta.PENDENTE

    # Snapshot do cliente
    cliente_nome: str
    cliente_cpf_cnpj: str
    cliente_email: str = ""
    cliente_telefone: str = ""
    cliente_endereco: str = ""
    cliente_cidade: str = ""
    cliente_estado: str = ""
    cliente_cep: str = ""

    # Dimensionamento
    potencia_sistema_kwp: Decimal
    quantidade_paineis: int
    painel_modelo: str
    inversor_modelo: str
    geracao_mensal_kwh: Decimal

    # Financeiro
    valor_final: Decimal
    forma_pagamento: str
    numero_parcelas: int = 0
    valor_parcela: Decimal = Decimal("0")
    taxa_juros: Decimal = Decimal("0")

    data_validade: date
    observacoes: str = ""

    def pode_aceitar(self) -> bool:
        return self.status == StatusProposta.PENDENTE

    def aceitar(self) -> None:
        if not self.pode_aceitar():
            raise ValueError("Proposta não pode ser aceita no status atual")
        self.status = StatusProposta.ACEITA
        self.updated_at = datetime.now(timezone.utc)

    def recusar(self) -> None:
        if self.status != StatusProposta.PENDENTE:
            raise ValueError("Proposta não pode ser recusada no status atual")
        self.status = StatusProposta.RECUSADA
        self.updated_at = datetime.now(timezone.utc)
