from enum import Enum
from uuid import UUID

from src.shared.base_entity import TenantEntity


class TipoTemplate(str, Enum):
    ORCAMENTO = "orcamento"
    PROPOSTA = "proposta"
    CONTRATO = "contrato"


class Template(TenantEntity):
    nome: str
    tipo: TipoTemplate
    arquivo_path: str
    tamanho_bytes: int = 0
    variaveis_encontradas: list[str] = []
    ativo: bool = True
