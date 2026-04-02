from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, EmailStr


class CriarVendedorRequest(BaseModel):
    nome: str
    email: EmailStr
    password: str
    role: str = "vendedor"  # vendedor | indicacao


class AtualizarVendedorRequest(BaseModel):
    nome: str | None = None
    role: str | None = None


class ResetarSenhaRequest(BaseModel):
    nova_senha: str


class VendedorResponse(BaseModel):
    id: UUID
    tenant_id: UUID
    email: str
    nome: str
    role: str
    ativo: bool
    bloqueado: bool

    model_config = {"from_attributes": True}


class ResumoVendedorResponse(BaseModel):
    vendedor_id: UUID
    nome: str
    total_clientes: int
    total_contratos: int
    valor_total_vendas: Decimal
    comissao_estimada: Decimal
