from uuid import UUID

from src.clientes.application.dtos import AtualizarClienteRequest, CriarClienteRequest
from src.clientes.domain.entities import Cliente, StatusCliente
from src.clientes.domain.repositories import ClienteRepository
from src.shared.exceptions import ForbiddenError, NotFoundError
from src.shared.value_objects import validate_cpf_cnpj


class CriarClienteUseCase:
    def __init__(self, repo: ClienteRepository):
        self.repo = repo

    async def execute(
        self, dto: CriarClienteRequest, tenant_id: UUID, user_role: str, user_id: UUID
    ) -> Cliente:
        cpf_cnpj = validate_cpf_cnpj(dto.cpf_cnpj)
        vendedor_id = dto.vendedor_id if user_role == "admin" else user_id

        cliente = Cliente(
            tenant_id=tenant_id,
            vendedor_id=vendedor_id,
            nome=dto.nome,
            cpf_cnpj=cpf_cnpj,
            telefone=dto.telefone,
            email=dto.email,
            endereco=dto.endereco,
            bairro=dto.bairro,
            cidade=dto.cidade,
            estado=dto.estado,
            cep=dto.cep,
        )
        return await self.repo.create(cliente)


class ListarClientesUseCase:
    def __init__(self, repo: ClienteRepository):
        self.repo = repo

    async def execute(
        self,
        tenant_id: UUID,
        user_role: str,
        user_id: UUID,
        status: str | None = None,
        offset: int = 0,
        limit: int = 20,
    ) -> tuple[list[Cliente], int]:
        vendedor_id = None if user_role == "admin" else user_id
        items = await self.repo.list_by_tenant(
            tenant_id, vendedor_id=vendedor_id, status=status, offset=offset, limit=limit
        )
        total = await self.repo.count_by_tenant(
            tenant_id, vendedor_id=vendedor_id, status=status
        )
        return items, total


class ObterClienteUseCase:
    def __init__(self, repo: ClienteRepository):
        self.repo = repo

    async def execute(
        self, cliente_id: UUID, tenant_id: UUID, user_role: str, user_id: UUID
    ) -> Cliente:
        cliente = await self.repo.get_by_id(cliente_id, tenant_id)
        if not cliente:
            raise NotFoundError("Cliente", str(cliente_id))
        if user_role != "admin" and cliente.vendedor_id != user_id:
            raise ForbiddenError("Voce nao tem acesso a este cliente")
        return cliente


class AtualizarClienteUseCase:
    def __init__(self, repo: ClienteRepository):
        self.repo = repo

    async def execute(
        self,
        cliente_id: UUID,
        dto: AtualizarClienteRequest,
        tenant_id: UUID,
        user_role: str,
        user_id: UUID,
    ) -> Cliente:
        cliente = await self.repo.get_by_id(cliente_id, tenant_id)
        if not cliente:
            raise NotFoundError("Cliente", str(cliente_id))
        if user_role != "admin" and cliente.vendedor_id != user_id:
            raise ForbiddenError("Voce nao tem acesso a este cliente")

        updates = dto.model_dump(exclude_unset=True)
        if "cpf_cnpj" in updates:
            updates["cpf_cnpj"] = validate_cpf_cnpj(updates["cpf_cnpj"])
        for key, value in updates.items():
            setattr(cliente, key, value)
        return await self.repo.update(cliente)


class DeletarClienteUseCase:
    def __init__(self, repo: ClienteRepository):
        self.repo = repo

    async def execute(self, cliente_id: UUID, tenant_id: UUID) -> bool:
        cliente = await self.repo.get_by_id(cliente_id, tenant_id)
        if not cliente:
            raise NotFoundError("Cliente", str(cliente_id))
        return await self.repo.delete(cliente_id, tenant_id)
