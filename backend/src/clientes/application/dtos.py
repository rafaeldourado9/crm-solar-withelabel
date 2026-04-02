from uuid import UUID

from pydantic import BaseModel

from src.clientes.domain.entities import StatusCliente


class CriarClienteRequest(BaseModel):
    nome: str
    cpf_cnpj: str
    telefone: str = ""
    email: str = ""
    endereco: str = ""
    bairro: str = ""
    cidade: str = ""
    estado: str = ""
    cep: str = ""
    vendedor_id: UUID | None = None


class AtualizarClienteRequest(BaseModel):
    nome: str | None = None
    cpf_cnpj: str | None = None
    telefone: str | None = None
    email: str | None = None
    endereco: str | None = None
    bairro: str | None = None
    cidade: str | None = None
    estado: str | None = None
    cep: str | None = None


class ClienteResponse(BaseModel):
    id: UUID
    tenant_id: UUID
    vendedor_id: UUID | None
    nome: str
    cpf_cnpj: str
    telefone: str
    email: str
    endereco: str
    bairro: str
    cidade: str
    estado: str
    cep: str
    status: str
    ativo: bool

    model_config = {"from_attributes": True}


class ClienteListResponse(BaseModel):
    items: list[ClienteResponse]
    total: int
    offset: int
    limit: int
