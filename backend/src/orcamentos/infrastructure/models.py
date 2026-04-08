from sqlalchemy import Boolean, ForeignKey, Integer, JSON, Numeric, String
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column

from src.shared.base_model import BaseModel


class OrcamentoModel(BaseModel):
    __tablename__ = "orcamentos"

    tenant_id: Mapped[PG_UUID] = mapped_column(
        PG_UUID(as_uuid=True), ForeignKey("tenants.id"), index=True
    )
    cliente_id: Mapped[PG_UUID] = mapped_column(
        PG_UUID(as_uuid=True), ForeignKey("clientes.id"), index=True
    )
    vendedor_id: Mapped[PG_UUID | None] = mapped_column(
        PG_UUID(as_uuid=True), ForeignKey("users.id"), nullable=True, index=True
    )
    status: Mapped[str] = mapped_column(String(20), default="rascunho")

    # Dimensionamento
    consumo_mensal_kwh: Mapped[Numeric] = mapped_column(Numeric(10, 2))
    painel_id: Mapped[PG_UUID] = mapped_column(PG_UUID(as_uuid=True))
    painel_modelo: Mapped[str] = mapped_column(String(200), default="")
    painel_potencia_w: Mapped[int] = mapped_column(Integer, default=0)
    inversor_id: Mapped[PG_UUID] = mapped_column(PG_UUID(as_uuid=True))
    inversor_modelo: Mapped[str] = mapped_column(String(200), default="")
    inversor_potencia_nominal_w: Mapped[int] = mapped_column(Integer, default=0)
    quantidade_paineis: Mapped[int] = mapped_column(Integer, default=0)
    potencia_sistema_kwp: Mapped[Numeric] = mapped_column(Numeric(10, 3), default=0)
    geracao_mensal_kwh: Mapped[Numeric] = mapped_column(Numeric(10, 2), default=0)

    # Custos
    valor_kit: Mapped[Numeric] = mapped_column(Numeric(12, 2), default=0)
    valor_montagem: Mapped[Numeric] = mapped_column(Numeric(10, 2), default=0)
    valor_projeto: Mapped[Numeric] = mapped_column(Numeric(10, 2), default=0)
    valor_estrutura: Mapped[Numeric] = mapped_column(Numeric(10, 2), default=0)
    tipo_estrutura: Mapped[str] = mapped_column(String(30), default="ceramico")
    valor_material_eletrico: Mapped[Numeric] = mapped_column(Numeric(10, 2), default=0)
    custo_deslocamento: Mapped[Numeric] = mapped_column(Numeric(10, 2), default=0)
    itens_adicionais: Mapped[list] = mapped_column(JSON, default=list)
    valor_itens_adicionais: Mapped[Numeric] = mapped_column(Numeric(10, 2), default=0)
    subtotal: Mapped[Numeric] = mapped_column(Numeric(12, 2), default=0)

    # Margens
    margem_lucro: Mapped[Numeric] = mapped_column(Numeric(5, 2), default=18)
    comissao: Mapped[Numeric] = mapped_column(Numeric(5, 2), default=5)
    imposto: Mapped[Numeric] = mapped_column(Numeric(5, 2), default=6)
    margem_desconto_avista: Mapped[Numeric] = mapped_column(Numeric(5, 2), default=2)

    # Valores finais
    valor_final: Mapped[Numeric] = mapped_column(Numeric(12, 2), default=0)
    forma_pagamento: Mapped[str] = mapped_column(String(10), default="avista")
    taxa_juros: Mapped[Numeric] = mapped_column(Numeric(5, 2), default=0)
    valor_cobrado: Mapped[Numeric] = mapped_column(Numeric(12, 2), default=0)
    numero_parcelas: Mapped[int] = mapped_column(Integer, default=0)
    valor_parcela: Mapped[Numeric] = mapped_column(Numeric(12, 2), default=0)

    # Economia
    economia_25_anos: Mapped[list] = mapped_column(JSON, default=list)
