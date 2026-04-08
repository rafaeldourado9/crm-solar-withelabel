from decimal import Decimal

from pydantic import BaseModel


class CalcularDeslocamentoRequest(BaseModel):
    cidade_cliente: str
    endereco_cliente: str = ""
    distancia_km: Decimal | None = None  # se None, usa provider para calcular


class DeslocamentoResponse(BaseModel):
    distancia_km: Decimal
    custo: Decimal
    cidade_isenta: bool
