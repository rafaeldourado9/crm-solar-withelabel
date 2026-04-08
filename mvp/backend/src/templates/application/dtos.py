from uuid import UUID

from pydantic import BaseModel


class TemplateResponse(BaseModel):
    id: UUID
    tenant_id: UUID
    nome: str
    tipo: str
    arquivo_path: str
    tamanho_bytes: int
    variaveis_encontradas: list[str]
    ativo: bool

    model_config = {"from_attributes": True}
