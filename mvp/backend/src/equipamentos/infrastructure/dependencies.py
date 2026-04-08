from decimal import Decimal

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_db
from src.equipamentos.application.use_cases import (
    CriarInversorUseCase,
    CriarPainelUseCase,
    ListarInversoresUseCase,
    ListarPaineisUseCase,
    ValidarDimensionamentoUseCase,
)
from src.equipamentos.domain.repositories import InversorRepository, PainelRepository
from src.equipamentos.infrastructure.repositories import (
    SQLAlchemyInversorRepository,
    SQLAlchemyPainelRepository,
)


def get_painel_repository(db: AsyncSession = Depends(get_db)) -> PainelRepository:
    return SQLAlchemyPainelRepository(db)


def get_inversor_repository(db: AsyncSession = Depends(get_db)) -> InversorRepository:
    return SQLAlchemyInversorRepository(db)


def get_criar_painel_use_case(
    repo: PainelRepository = Depends(get_painel_repository),
) -> CriarPainelUseCase:
    return CriarPainelUseCase(repo)


def get_listar_paineis_use_case(
    repo: PainelRepository = Depends(get_painel_repository),
) -> ListarPaineisUseCase:
    return ListarPaineisUseCase(repo)


def get_criar_inversor_use_case(
    repo: InversorRepository = Depends(get_inversor_repository),
) -> CriarInversorUseCase:
    return CriarInversorUseCase(repo)


def get_listar_inversores_use_case(
    repo: InversorRepository = Depends(get_inversor_repository),
) -> ListarInversoresUseCase:
    return ListarInversoresUseCase(repo)


def get_validar_dimensionamento_use_case(
    painel_repo: PainelRepository = Depends(get_painel_repository),
    inversor_repo: InversorRepository = Depends(get_inversor_repository),
) -> ValidarDimensionamentoUseCase:
    return ValidarDimensionamentoUseCase(painel_repo, inversor_repo, Decimal("0.70"))
