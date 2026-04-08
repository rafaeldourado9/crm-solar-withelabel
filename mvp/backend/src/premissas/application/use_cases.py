from uuid import UUID

from src.premissas.application.dtos import AtualizarPremissaRequest
from src.premissas.domain.entities import Premissa
from src.premissas.domain.repositories import PremissaRepository
from src.shared.exceptions import NotFoundError


class ObterPremissaAtivaUseCase:
    def __init__(self, repo: PremissaRepository):
        self.repo = repo

    async def execute(self, tenant_id: UUID) -> Premissa:
        premissa = await self.repo.get_ativa(tenant_id)
        if not premissa:
            # Criar premissa default se não existir
            premissa = Premissa(tenant_id=tenant_id)
            premissa = await self.repo.create(premissa)
        return premissa


class AtualizarPremissaUseCase:
    def __init__(self, repo: PremissaRepository):
        self.repo = repo

    async def execute(self, premissa_id: UUID, dto: AtualizarPremissaRequest) -> Premissa:
        premissa = await self.repo.get_by_id(premissa_id)
        if not premissa:
            raise NotFoundError("Premissa", str(premissa_id))

        updates = dto.model_dump(exclude_unset=True)
        for key, value in updates.items():
            setattr(premissa, key, value)

        return await self.repo.update(premissa)
