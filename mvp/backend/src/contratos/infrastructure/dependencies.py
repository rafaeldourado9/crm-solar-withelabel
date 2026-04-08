from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.contratos.application.use_cases import (
    AtualizarContratoUseCase,
    CriarContratoUseCase,
    ListarContratosUseCase,
    ObterContratoUseCase,
)
from src.contratos.infrastructure.repositories import SQLAlchemyContratoRepository
from src.database import get_db
from src.propostas.infrastructure.repositories import SQLAlchemyPropostaRepository
from src.tenant.infrastructure.repositories import SQLAlchemyTenantRepository


def get_criar_contrato_use_case(db: AsyncSession = Depends(get_db)) -> CriarContratoUseCase:
    return CriarContratoUseCase(
        contrato_repo=SQLAlchemyContratoRepository(db),
        proposta_repo=SQLAlchemyPropostaRepository(db),
        tenant_repo=SQLAlchemyTenantRepository(db),
    )


def get_listar_contratos_use_case(db: AsyncSession = Depends(get_db)) -> ListarContratosUseCase:
    return ListarContratosUseCase(SQLAlchemyContratoRepository(db))


def get_obter_contrato_use_case(db: AsyncSession = Depends(get_db)) -> ObterContratoUseCase:
    return ObterContratoUseCase(SQLAlchemyContratoRepository(db))


def get_atualizar_contrato_use_case(db: AsyncSession = Depends(get_db)) -> AtualizarContratoUseCase:
    return AtualizarContratoUseCase(SQLAlchemyContratoRepository(db), session=db)
