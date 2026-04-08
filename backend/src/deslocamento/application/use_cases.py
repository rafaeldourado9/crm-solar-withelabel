from decimal import Decimal
from uuid import UUID

from src.deslocamento.application.dtos import CalcularDeslocamentoRequest, DeslocamentoResponse
from src.deslocamento.domain.ports import DistanceProvider
from src.deslocamento.domain.services import DeslocamentoCalculator
from src.premissas.domain.entities import Premissa
from src.premissas.domain.repositories import PremissaRepository
from src.shared.exceptions import ValidationError


class CalcularDeslocamentoUseCase:
    def __init__(
        self,
        premissa_repo: PremissaRepository,
        distance_provider: DistanceProvider,
    ):
        self.premissa_repo = premissa_repo
        self.distance_provider = distance_provider

    async def execute(
        self, dto: CalcularDeslocamentoRequest, tenant_id: UUID
    ) -> DeslocamentoResponse:
        premissa = await self.premissa_repo.get_ativa(tenant_id)
        if not premissa:
            raise ValidationError("Premissas nao configuradas para este tenant")

        if dto.distancia_km is not None:
            distancia = dto.distancia_km
        elif dto.endereco_cliente:
            distancia = Decimal(
                str(await self.distance_provider.get_distance_km("Dourados, MS", dto.endereco_cliente))
            )
        else:
            raise ValidationError("Informe distancia_km ou endereco_cliente")

        resultado = DeslocamentoCalculator.calcular(
            cidade_cliente=dto.cidade_cliente,
            distancia_km=distancia,
            consumo_veiculo=premissa.consumo_veiculo,
            preco_combustivel=premissa.preco_combustivel,
            margem_deslocamento=premissa.margem_deslocamento,
            cidades_sem_cobranca=premissa.cidades_sem_cobranca,
        )

        return DeslocamentoResponse(
            distancia_km=resultado.distancia_km,
            custo=resultado.custo,
            cidade_isenta=resultado.cidade_isenta,
        )
