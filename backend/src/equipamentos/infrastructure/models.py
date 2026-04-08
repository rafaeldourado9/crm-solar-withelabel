from sqlalchemy import Boolean, ForeignKey, Integer, Numeric, String
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column

from src.shared.base_model import BaseModel


class PainelModel(BaseModel):
    __tablename__ = "paineis"

    tenant_id: Mapped[PG_UUID] = mapped_column(
        PG_UUID(as_uuid=True), ForeignKey("tenants.id"), index=True
    )
    modelo: Mapped[str] = mapped_column(String(200))
    fabricante: Mapped[str] = mapped_column(String(200))
    potencia_w: Mapped[int] = mapped_column(Integer)
    eficiencia: Mapped[Numeric] = mapped_column(Numeric(5, 2))
    garantia_anos: Mapped[int] = mapped_column(Integer, default=25)
    preco: Mapped[Numeric] = mapped_column(Numeric(10, 2))
    ativo: Mapped[bool] = mapped_column(Boolean, default=True)


class InversorModel(BaseModel):
    __tablename__ = "inversores"

    tenant_id: Mapped[PG_UUID] = mapped_column(
        PG_UUID(as_uuid=True), ForeignKey("tenants.id"), index=True
    )
    modelo: Mapped[str] = mapped_column(String(200))
    fabricante: Mapped[str] = mapped_column(String(200))
    potencia_nominal_w: Mapped[int] = mapped_column(Integer)
    potencia_maxima_w: Mapped[int] = mapped_column(Integer)
    eficiencia: Mapped[Numeric] = mapped_column(Numeric(5, 2))
    garantia_anos: Mapped[int] = mapped_column(Integer, default=10)
    preco: Mapped[Numeric] = mapped_column(Numeric(10, 2))
    ativo: Mapped[bool] = mapped_column(Boolean, default=True)
