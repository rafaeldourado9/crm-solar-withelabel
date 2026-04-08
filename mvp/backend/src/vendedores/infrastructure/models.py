from sqlalchemy import Boolean, ForeignKey, Numeric
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column

from src.shared.base_model import TenantModel


class VendaVendedorModel(TenantModel):
    __tablename__ = "vendas_vendedor"

    contrato_id: Mapped[PG_UUID] = mapped_column(
        PG_UUID(as_uuid=True), ForeignKey("contratos.id"), unique=True, index=True
    )
    vendedor_id: Mapped[PG_UUID] = mapped_column(
        PG_UUID(as_uuid=True), ForeignKey("users.id"), index=True
    )
    valor_venda: Mapped[Numeric] = mapped_column(Numeric(12, 2))
    valor_comissao: Mapped[Numeric] = mapped_column(Numeric(12, 2))
    pago: Mapped[bool] = mapped_column(Boolean, default=False)
