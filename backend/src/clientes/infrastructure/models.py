from sqlalchemy import Boolean, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column

from src.shared.base_model import BaseModel


class ClienteModel(BaseModel):
    __tablename__ = "clientes"

    tenant_id: Mapped[PG_UUID] = mapped_column(
        PG_UUID(as_uuid=True), ForeignKey("tenants.id"), index=True
    )
    vendedor_id: Mapped[PG_UUID | None] = mapped_column(
        PG_UUID(as_uuid=True), ForeignKey("users.id"), nullable=True, index=True
    )
    nome: Mapped[str] = mapped_column(String(200))
    cpf_cnpj: Mapped[str] = mapped_column(String(14), index=True)
    telefone: Mapped[str] = mapped_column(String(20), default="")
    email: Mapped[str] = mapped_column(String(255), default="")
    endereco: Mapped[str] = mapped_column(String(300), default="")
    bairro: Mapped[str] = mapped_column(String(100), default="")
    cidade: Mapped[str] = mapped_column(String(100), default="")
    estado: Mapped[str] = mapped_column(String(2), default="")
    cep: Mapped[str] = mapped_column(String(9), default="")
    status: Mapped[str] = mapped_column(String(20), default="orcamento")
    ativo: Mapped[bool] = mapped_column(Boolean, default=True)
