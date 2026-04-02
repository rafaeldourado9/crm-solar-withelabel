from sqlalchemy import ForeignKey, Integer, Numeric, String
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column

from src.shared.base_model import BaseModel


class ContratoModel(BaseModel):
    __tablename__ = "contratos"

    tenant_id: Mapped[PG_UUID] = mapped_column(PG_UUID(as_uuid=True), ForeignKey("tenants.id"), index=True)
    proposta_id: Mapped[PG_UUID] = mapped_column(PG_UUID(as_uuid=True), ForeignKey("propostas.id"), unique=True, index=True)
    cliente_id: Mapped[PG_UUID] = mapped_column(PG_UUID(as_uuid=True), ForeignKey("clientes.id"), index=True)
    vendedor_id: Mapped[PG_UUID | None] = mapped_column(PG_UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    numero: Mapped[str] = mapped_column(String(30), index=True)
    status: Mapped[str] = mapped_column(String(20), default="rascunho")

    # Dados do cliente
    cliente_nome: Mapped[str] = mapped_column(String(200))
    cliente_cpf_cnpj: Mapped[str] = mapped_column(String(14), default="")
    cliente_endereco: Mapped[str] = mapped_column(String(300), default="")
    cliente_bairro: Mapped[str] = mapped_column(String(100), default="")
    cliente_cidade: Mapped[str] = mapped_column(String(100), default="")
    cliente_estado: Mapped[str] = mapped_column(String(2), default="")
    cliente_cep: Mapped[str] = mapped_column(String(9), default="")

    # Dados da empresa (Tenant)
    empresa_razao_social: Mapped[str] = mapped_column(String(200))
    empresa_cnpj: Mapped[str] = mapped_column(String(18), default="")
    empresa_endereco: Mapped[str] = mapped_column(String(300), default="")
    empresa_cidade: Mapped[str] = mapped_column(String(100), default="")
    empresa_cep: Mapped[str] = mapped_column(String(9), default="")
    empresa_representante_nome: Mapped[str] = mapped_column(String(200), default="")
    empresa_representante_cpf: Mapped[str] = mapped_column(String(14), default="")
    empresa_representante_rg: Mapped[str] = mapped_column(String(20), default="")

    # Dados bancários
    banco_nome: Mapped[str] = mapped_column(String(100), default="")
    banco_agencia: Mapped[str] = mapped_column(String(20), default="")
    banco_conta: Mapped[str] = mapped_column(String(30), default="")
    banco_titular: Mapped[str] = mapped_column(String(200), default="")

    # Equipamentos / Valores
    potencia_total_kwp: Mapped[Numeric] = mapped_column(Numeric(10, 3), default=0)
    quantidade_paineis: Mapped[int] = mapped_column(Integer, default=0)
    valor_total: Mapped[Numeric] = mapped_column(Numeric(12, 2), default=0)
    numero_parcelas: Mapped[int] = mapped_column(Integer, default=0)
    valor_parcela: Mapped[Numeric] = mapped_column(Numeric(12, 2), default=0)

    # Termos
    prazo_execucao_dias: Mapped[int] = mapped_column(Integer, default=30)
    garantia_instalacao_meses: Mapped[int] = mapped_column(Integer, default=12)
    foro_comarca: Mapped[str] = mapped_column(String(100), default="")
