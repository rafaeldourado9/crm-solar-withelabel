from decimal import Decimal
from uuid import UUID

from pydantic import Field

from src.shared.base_entity import BaseEntity


class Painel(BaseEntity):
    tenant_id: UUID
    modelo: str
    fabricante: str
    potencia_w: int = Field(gt=0)
    eficiencia: Decimal = Field(gt=0, le=100)
    garantia_anos: int = Field(default=25)
    preco: Decimal = Field(gt=0)
    ativo: bool = True


class Inversor(BaseEntity):
    tenant_id: UUID
    modelo: str
    fabricante: str
    potencia_nominal_w: int = Field(gt=0)
    potencia_maxima_w: int = Field(gt=0)
    eficiencia: Decimal = Field(gt=0, le=100)
    garantia_anos: int = Field(default=10)
    preco: Decimal = Field(gt=0)
    ativo: bool = True

    def potencia_maxima_com_overload(self, overload: Decimal) -> int:
        """Calcula potência máxima considerando overload"""
        return int(self.potencia_nominal_w * (1 + overload))
