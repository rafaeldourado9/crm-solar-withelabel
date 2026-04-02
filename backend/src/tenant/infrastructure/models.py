from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from src.shared.base_model import BaseModel


class TenantModel(BaseModel):
    __tablename__ = "tenants"

    nome_fantasia: Mapped[str] = mapped_column(String(200))
    razao_social: Mapped[str] = mapped_column(String(200))
    cnpj: Mapped[str] = mapped_column(String(18), unique=True, index=True)
    endereco: Mapped[str] = mapped_column(String(300))
    cidade: Mapped[str] = mapped_column(String(100))
    estado: Mapped[str] = mapped_column(String(2))
    cep: Mapped[str] = mapped_column(String(9))
    representante_nome: Mapped[str] = mapped_column(String(200))
    representante_cpf: Mapped[str] = mapped_column(String(14))
    representante_rg: Mapped[str] = mapped_column(String(20), default="")
    banco_nome: Mapped[str] = mapped_column(String(100), default="")
    banco_agencia: Mapped[str] = mapped_column(String(10), default="")
    banco_conta: Mapped[str] = mapped_column(String(20), default="")
    banco_titular: Mapped[str] = mapped_column(String(200), default="")
    logo_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    cor_primaria: Mapped[str] = mapped_column(String(7), default="#1E40AF")
    cor_secundaria: Mapped[str] = mapped_column(String(7), default="#F59E0B")
    dominio_customizado: Mapped[str | None] = mapped_column(String(200), nullable=True)
    plano: Mapped[str] = mapped_column(String(20), default="free")
    ativo: Mapped[bool] = mapped_column(default=True)
