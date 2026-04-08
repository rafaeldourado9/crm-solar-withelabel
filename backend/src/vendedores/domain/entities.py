from decimal import Decimal
from uuid import UUID

from src.shared.base_entity import TenantEntity


class VendaVendedor(TenantEntity):
    contrato_id: UUID
    vendedor_id: UUID
    valor_venda: Decimal
    valor_comissao: Decimal
    pago: bool = False

    @classmethod
    def calcular(
        cls,
        tenant_id: UUID,
        contrato_id: UUID,
        vendedor_id: UUID,
        valor_venda: Decimal,
        comissao_percentual: Decimal,
    ) -> "VendaVendedor":
        valor_comissao = (valor_venda * comissao_percentual / 100).quantize(Decimal("0.01"))
        return cls(
            tenant_id=tenant_id,
            contrato_id=contrato_id,
            vendedor_id=vendedor_id,
            valor_venda=valor_venda,
            valor_comissao=valor_comissao,
        )
