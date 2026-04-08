from datetime import date
from sqlalchemy import Boolean, Date, ForeignKey, Integer, Numeric, String
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column

from src.shared.base_model import BaseModel


class PropostaModel(BaseModel):
    __tablename__ = "propostas"

    tenant_id: Mapped[PG_UUID] = mapped_column(PG_UUID(as_uuid=True), ForeignKey("tenants.id"), index=True)
    orcamento_id: Mapped[PG_UUID] = mapped_column(PG_UUID(as_uuid=True), ForeignKey("orcamentos.id"), index=True)
    cliente_id: Mapped[PG_UUID] = mapped_column(PG_UUID(as_uuid=True), ForeignKey("clientes.id"), index=True)
    vendedor_id: Mapped[PG_UUID | None] = mapped_column(PG_UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    numero: Mapped[str] = mapped_column(String(30), index=True)
    status: Mapped[str] = mapped_column(String(20), default="pendente")

    # Snapshot cliente
    cliente_nome: Mapped[str] = mapped_column(String(200))
    cliente_cpf_cnpj: Mapped[str] = mapped_column(String(14), default="")
    cliente_email: Mapped[str] = mapped_column(String(255), default="")
    cliente_telefone: Mapped[str] = mapped_column(String(20), default="")
    cliente_endereco: Mapped[str] = mapped_column(String(300), default="")
    cliente_cidade: Mapped[str] = mapped_column(String(100), default="")
    cliente_estado: Mapped[str] = mapped_column(String(2), default="")
    cliente_cep: Mapped[str] = mapped_column(String(9), default="")

    # Dimensionamento
    potencia_sistema_kwp: Mapped[Numeric] = mapped_column(Numeric(10, 3), default=0)
    quantidade_paineis: Mapped[int] = mapped_column(Integer, default=0)
    painel_modelo: Mapped[str] = mapped_column(String(200), default="")
    inversor_modelo: Mapped[str] = mapped_column(String(200), default="")
    geracao_mensal_kwh: Mapped[Numeric] = mapped_column(Numeric(10, 2), default=0)

    # Financeiro
    valor_final: Mapped[Numeric] = mapped_column(Numeric(12, 2), default=0)
    forma_pagamento: Mapped[str] = mapped_column(String(10), default="avista")
    numero_parcelas: Mapped[int] = mapped_column(Integer, default=0)
    valor_parcela: Mapped[Numeric] = mapped_column(Numeric(12, 2), default=0)
    taxa_juros: Mapped[Numeric] = mapped_column(Numeric(5, 2), default=0)

    data_validade: Mapped[date] = mapped_column(Date)
    observacoes: Mapped[str] = mapped_column(String(1000), default="")
