from uuid import UUID

from pydantic import BaseModel, EmailStr


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class LoginResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class RefreshRequest(BaseModel):
    refresh_token: str


class RefreshResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class CriarUserRequest(BaseModel):
    email: EmailStr
    password: str
    nome: str
    role: str = "vendedor"


class UserResponse(BaseModel):
    id: UUID
    tenant_id: UUID
    email: str
    nome: str
    role: str
    ativo: bool
    bloqueado: bool

    model_config = {"from_attributes": True}
