from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.clientes.application.use_cases import (
    AtualizarClienteUseCase,
    CriarClienteUseCase,
    DeletarClienteUseCase,
    ListarClientesUseCase,
    ObterClienteUseCase,
)
from src.clientes.domain.repositories import ClienteRepository
from src.clientes.infrastructure.repositories import SQLAlchemyClienteRepository
from src.database import get_db


def get_cliente_repository(db: AsyncSession = Depends(get_db)) -> ClienteRepository:
    return SQLAlchemyClienteRepository(db)


def get_criar_cliente_use_case(
    repo: ClienteRepository = Depends(get_cliente_repository),
) -> CriarClienteUseCase:
    return CriarClienteUseCase(repo)


def get_listar_clientes_use_case(
    repo: ClienteRepository = Depends(get_cliente_repository),
) -> ListarClientesUseCase:
    return ListarClientesUseCase(repo)


def get_obter_cliente_use_case(
    repo: ClienteRepository = Depends(get_cliente_repository),
) -> ObterClienteUseCase:
    return ObterClienteUseCase(repo)


def get_atualizar_cliente_use_case(
    repo: ClienteRepository = Depends(get_cliente_repository),
) -> AtualizarClienteUseCase:
    return AtualizarClienteUseCase(repo)


def get_deletar_cliente_use_case(
    repo: ClienteRepository = Depends(get_cliente_repository),
) -> DeletarClienteUseCase:
    return DeletarClienteUseCase(repo)
