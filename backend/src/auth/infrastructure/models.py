from sqlalchemy import Boolean, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column

from src.shared.base_model import BaseModel


class UserModel(BaseModel):
    __tablename__ = "users"

    tenant_id: Mapped[PG_UUID] = mapped_column(
        PG_UUID(as_uuid=True), ForeignKey("tenants.id"), index=True
    )
    email: Mapped[str] = mapped_column(String(255), index=True)
    hashed_password: Mapped[str] = mapped_column(String(255))
    nome: Mapped[str] = mapped_column(String(200))
    role: Mapped[str] = mapped_column(String(20), default="vendedor")
    ativo: Mapped[bool] = mapped_column(Boolean, default=True)
    bloqueado: Mapped[bool] = mapped_column(Boolean, default=False)
