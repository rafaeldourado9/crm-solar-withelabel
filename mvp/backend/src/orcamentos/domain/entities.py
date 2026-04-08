from decimal import Decimal
from enum import StrEnum
from uuid import UUID

from pydantic import Field

from src.shared.base_entity import BaseEntity


class StatusOrcamento(StrEnum):
    RASCUNHO = "rascunho"
    FINALIZADO = "finalizado"
    CONVERTIDO = "convertido"


class ItemAdicional(BaseEntity):
    descricao: str
    valor: Decimal


class Orcamento(BaseEntity):
    tenant_id: UUID
    cliente_id: UUID
    vendedor_id: UUID | None = None
    status: StatusOrcamento = StatusOrcamento.RASCUNHO

    # Dimensionamento
    consumo_mensal_kwh: Decimal
    painel_id: UUID
    painel_modelo: str = ""
    painel_potencia_w: int = 0
    inversor_id: UUID
    inversor_modelo: str = ""
    inversor_potencia_nominal_w: int = 0
    quantidade_paineis: int = 0
    potencia_sistema_kwp: Decimal = Decimal("0")
    geracao_mensal_kwh: Decimal = Decimal("0")

    # Custos
    valor_kit: Decimal = Decimal("0")
    valor_montagem: Decimal = Decimal("0")
    valor_projeto: Decimal = Decimal("0")
    valor_estrutura: Decimal = Decimal("0")
    tipo_estrutura: str = "ceramico"
    valor_material_eletrico: Decimal = Decimal("0")
    custo_deslocamento: Decimal = Decimal("0")
    itens_adicionais: list[dict] = Field(default_factory=list)
    valor_itens_adicionais: Decimal = Decimal("0")
    subtotal: Decimal = Decimal("0")

    # Margens
    margem_lucro: Decimal = Decimal("18")
    comissao: Decimal = Decimal("5")
    imposto: Decimal = Decimal("6")
    margem_desconto_avista: Decimal = Decimal("2")

    # Valores finais
    valor_final: Decimal = Decimal("0")
    forma_pagamento: str = "avista"
    taxa_juros: Decimal = Decimal("0")
    valor_cobrado: Decimal = Decimal("0")
    numero_parcelas: int = 0
    valor_parcela: Decimal = Decimal("0")

    # Economia
    economia_25_anos: list[dict] = Field(default_factory=list)
