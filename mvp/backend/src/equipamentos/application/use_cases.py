from decimal import Decimal
from uuid import UUID

from src.equipamentos.application.dtos import (
    CriarInversorRequest,
    CriarPainelRequest,
    ValidarDimensionamentoRequest,
)
from src.equipamentos.domain.entities import Inversor, Painel
from src.equipamentos.domain.repositories import InversorRepository, PainelRepository
from src.equipamentos.domain.services import ValidacaoDimensionamentoService
from src.shared.exceptions import NotFoundError


class CriarPainelUseCase:
    def __init__(self, repo: PainelRepository):
        self.repo = repo

    async def execute(self, dto: CriarPainelRequest, tenant_id: UUID) -> Painel:
        painel = Painel(tenant_id=tenant_id, **dto.model_dump())
        return await self.repo.create(painel)


class ListarPaineisUseCase:
    def __init__(self, repo: PainelRepository):
        self.repo = repo

    async def execute(self, tenant_id: UUID) -> list[Painel]:
        return await self.repo.list_ativos(tenant_id)


class CriarInversorUseCase:
    def __init__(self, repo: InversorRepository):
        self.repo = repo

    async def execute(self, dto: CriarInversorRequest, tenant_id: UUID) -> Inversor:
        inversor = Inversor(tenant_id=tenant_id, **dto.model_dump())
        return await self.repo.create(inversor)


class ListarInversoresUseCase:
    def __init__(self, repo: InversorRepository):
        self.repo = repo

    async def execute(self, tenant_id: UUID) -> list[Inversor]:
        return await self.repo.list_ativos(tenant_id)


class ValidarDimensionamentoUseCase:
    def __init__(
        self,
        painel_repo: PainelRepository,
        inversor_repo: InversorRepository,
        overload: Decimal,
    ):
        self.painel_repo = painel_repo
        self.inversor_repo = inversor_repo
        self.overload = overload

    async def execute(self, dto: ValidarDimensionamentoRequest, tenant_id: UUID) -> dict:
        painel = await self.painel_repo.get_by_id(dto.painel_id, tenant_id)
        if not painel:
            raise NotFoundError("Painel", str(dto.painel_id))

        inversor = await self.inversor_repo.get_by_id(dto.inversor_id, tenant_id)
        if not inversor:
            raise NotFoundError("Inversor", str(dto.inversor_id))

        try:
            ValidacaoDimensionamentoService.validar_painel_inversor(
                dto.quantidade_paineis, painel, inversor, self.overload
            )
            return {"valido": True, "mensagem": "Dimensionamento válido"}
        except Exception as e:
            return {"valido": False, "mensagem": str(e)}
