from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel


class CriarPainelRequest(BaseModel):
    modelo: str
    fabricante: str
    potencia_w: int
    eficiencia: Decimal
    garantia_anos: int = 25
    preco: Decimal


class CriarInversorRequest(BaseModel):
    modelo: str
    fabricante: str
    potencia_nominal_w: int
    potencia_maxima_w: int
    eficiencia: Decimal
    garantia_anos: int = 10
    preco: Decimal


class PainelResponse(BaseModel):
    id: UUID
    tenant_id: UUID
    modelo: str
    fabricante: str
    potencia_w: int
    eficiencia: Decimal
    garantia_anos: int
    preco: Decimal
    ativo: bool

    model_config = {"from_attributes": True}


class InversorResponse(BaseModel):
    id: UUID
    tenant_id: UUID
    modelo: str
    fabricante: str
    potencia_nominal_w: int
    potencia_maxima_w: int
    eficiencia: Decimal
    garantia_anos: int
    preco: Decimal
    ativo: bool

    model_config = {"from_attributes": True}


class ValidarDimensionamentoRequest(BaseModel):
    quantidade_paineis: int
    painel_id: UUID
    inversor_id: UUID


class ValidarDimensionamentoResponse(BaseModel):
    valido: bool
    mensagem: str
