from uuid import UUID

from pydantic import BaseModel, Field


class CriarTenantRequest(BaseModel):
    nome_fantasia: str
    razao_social: str
    cnpj: str
    endereco: str
    cidade: str
    estado: str = Field(max_length=2)
    cep: str
    representante_nome: str
    representante_cpf: str
    representante_rg: str = ""
    banco_nome: str = ""
    banco_agencia: str = ""
    banco_conta: str = ""
    banco_titular: str = ""


class AtualizarTenantRequest(BaseModel):
    nome_fantasia: str | None = None
    razao_social: str | None = None
    endereco: str | None = None
    cidade: str | None = None
    estado: str | None = None
    cep: str | None = None
    representante_nome: str | None = None
    representante_cpf: str | None = None
    representante_rg: str | None = None
    banco_nome: str | None = None
    banco_agencia: str | None = None
    banco_conta: str | None = None
    banco_titular: str | None = None


class AtualizarBrandingRequest(BaseModel):
    logo_url: str | None = None
    cor_primaria: str | None = None
    cor_secundaria: str | None = None
    dominio_customizado: str | None = None


class TenantResponse(BaseModel):
    id: UUID
    nome_fantasia: str
    razao_social: str
    cnpj: str
    endereco: str
    cidade: str
    estado: str
    cep: str
    representante_nome: str
    representante_cpf: str
    representante_rg: str
    banco_nome: str
    banco_agencia: str
    banco_conta: str
    banco_titular: str
    logo_url: str | None
    cor_primaria: str
    cor_secundaria: str
    dominio_customizado: str | None
    plano: str
    ativo: bool

    model_config = {"from_attributes": True}
