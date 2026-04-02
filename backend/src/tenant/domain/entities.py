from uuid import UUID

from pydantic import Field

from src.shared.base_entity import BaseEntity


class Tenant(BaseEntity):
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
    logo_url: str | None = None
    cor_primaria: str = "#1E40AF"
    cor_secundaria: str = "#F59E0B"
    dominio_customizado: str | None = None
    plano: str = "free"  # free, pro, enterprise
    ativo: bool = True
