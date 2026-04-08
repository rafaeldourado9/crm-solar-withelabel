from uuid import UUID

from pydantic import EmailStr, Field

from src.shared.base_entity import BaseEntity


class User(BaseEntity):
    tenant_id: UUID
    email: EmailStr
    hashed_password: str
    nome: str
    role: str = Field(default="vendedor")  # admin, vendedor, indicacao
    ativo: bool = True
    bloqueado: bool = False
