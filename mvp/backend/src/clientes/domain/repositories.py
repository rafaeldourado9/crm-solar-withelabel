from typing import Protocol
from uuid import UUID

from src.clientes.domain.entities import Cliente


class ClienteRepository(Protocol):
    async def create(self, cliente: Cliente) -> Cliente: ...
    async def get_by_id(self, cliente_id: UUID, tenant_id: UUID) -> Cliente | None: ...
    async def list_by_tenant(
        self,
        tenant_id: UUID,
        vendedor_id: UUID | None = None,
        status: str | None = None,
        offset: int = 0,
        limit: int = 20,
    ) -> list[Cliente]: ...
    async def count_by_tenant(
        self,
        tenant_id: UUID,
        vendedor_id: UUID | None = None,
        status: str | None = None,
    ) -> int: ...
    async def update(self, cliente: Cliente) -> Cliente: ...
    async def delete(self, cliente_id: UUID, tenant_id: UUID) -> bool: ...
