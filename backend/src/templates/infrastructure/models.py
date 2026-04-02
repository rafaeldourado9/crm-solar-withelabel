from sqlalchemy import Boolean, ForeignKey, Integer, JSON, String
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column

from src.shared.base_model import BaseModel


class TemplateModel(BaseModel):
    __tablename__ = "templates_docx"

    tenant_id: Mapped[PG_UUID] = mapped_column(PG_UUID(as_uuid=True), ForeignKey("tenants.id"), index=True)
    nome: Mapped[str] = mapped_column(String(200))
    tipo: Mapped[str] = mapped_column(String(20), index=True)
    arquivo_path: Mapped[str] = mapped_column(String(500))
    tamanho_bytes: Mapped[int] = mapped_column(Integer, default=0)
    variaveis_encontradas: Mapped[list] = mapped_column(JSON, default=list)
    ativo: Mapped[bool] = mapped_column(Boolean, default=True)
