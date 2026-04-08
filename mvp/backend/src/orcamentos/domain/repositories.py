from typing import Protocol
from uuid import UUID

from src.orcamentos.domain.entities import Orcamento


class OrcamentoRepository(Protocol):
    async def create(self, orcamento: Orcamento) -> Orcamento: ...
    async def get_by_id(self, orcamento_id: UUID, tenant_id: UUID) -> Orcamento | None: ...
    async def list_by_tenant(
        self,
        tenant_id: UUID,
        vendedor_id: UUID | None = None,
        cliente_id: UUID | None = None,
        offset: int = 0,
        limit: int = 20,
    ) -> list[Orcamento]: ...
    async def count_by_tenant(
        self,
        tenant_id: UUID,
        vendedor_id: UUID | None = None,
        cliente_id: UUID | None = None,
    ) -> int: ...
    async def update(self, orcamento: Orcamento) -> Orcamento: ...
    async def delete(self, orcamento_id: UUID, tenant_id: UUID) -> bool: ...
