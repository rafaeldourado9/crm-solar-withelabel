from typing import Protocol
from uuid import UUID

from src.propostas.domain.entities import Proposta


class PropostaRepository(Protocol):
    async def create(self, proposta: Proposta) -> Proposta: ...
    async def get_by_id(self, id: UUID, tenant_id: UUID) -> Proposta | None: ...
    async def list_by_tenant(
        self,
        tenant_id: UUID,
        cliente_id: UUID | None = None,
        status: str | None = None,
        offset: int = 0,
        limit: int = 20,
    ) -> list[Proposta]: ...
    async def count_by_tenant(
        self, tenant_id: UUID, cliente_id: UUID | None = None, status: str | None = None
    ) -> int: ...
    async def update(self, proposta: Proposta) -> Proposta: ...
    async def next_numero(self, tenant_id: UUID) -> str: ...
