from decimal import Decimal

from src.equipamentos.domain.entities import Inversor, Painel
from src.shared.exceptions import ValidationError


class ValidacaoDimensionamentoService:
    @staticmethod
    def validar_painel_inversor(
        quantidade_paineis: int,
        painel: Painel,
        inversor: Inversor,
        overload: Decimal,
    ) -> bool:
        """Valida se a potência dos painéis não excede a capacidade do inversor"""
        potencia_paineis_total = quantidade_paineis * painel.potencia_w
        potencia_maxima_inversor = inversor.potencia_maxima_com_overload(overload)

        if potencia_paineis_total > potencia_maxima_inversor:
            raise ValidationError(
                f"Potência dos painéis ({potencia_paineis_total}W) excede "
                f"capacidade do inversor ({potencia_maxima_inversor}W com overload)"
            )

        return True
