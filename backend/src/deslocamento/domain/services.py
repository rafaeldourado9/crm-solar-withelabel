from decimal import Decimal
from dataclasses import dataclass


@dataclass(frozen=True)
class ResultadoDeslocamento:
    distancia_km: Decimal
    custo: Decimal
    cidade_isenta: bool


class DeslocamentoCalculator:
    """Logica pura de calculo de deslocamento - sem dependencias externas."""

    @staticmethod
    def calcular(
        cidade_cliente: str,
        distancia_km: Decimal,
        consumo_veiculo: Decimal,
        preco_combustivel: Decimal,
        margem_deslocamento: Decimal,
        cidades_sem_cobranca: list[str],
    ) -> ResultadoDeslocamento:
        cidade_normalizada = cidade_cliente.strip().lower()
        cidades_isentas = [c.strip().lower() for c in cidades_sem_cobranca]

        if cidade_normalizada in cidades_isentas:
            return ResultadoDeslocamento(
                distancia_km=Decimal("0"),
                custo=Decimal("0"),
                cidade_isenta=True,
            )

        distancia_total = distancia_km * 2  # ida e volta
        litros = distancia_total / consumo_veiculo
        custo_combustivel = litros * preco_combustivel
        custo = custo_combustivel * (1 + margem_deslocamento)

        return ResultadoDeslocamento(
            distancia_km=distancia_km,
            custo=custo.quantize(Decimal("0.01")),
            cidade_isenta=False,
        )
