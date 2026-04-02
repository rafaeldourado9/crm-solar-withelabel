from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_db
from src.premissas.application.use_cases import (
    AtualizarPremissaUseCase,
    ObterPremissaAtivaUseCase,
)
from src.premissas.domain.repositories import PremissaRepository
from src.premissas.infrastructure.repositories import SQLAlchemyPremissaRepository


def get_premissa_repository(db: AsyncSession = Depends(get_db)) -> PremissaRepository:
    return SQLAlchemyPremissaRepository(db)


def get_obter_premissa_ativa_use_case(
    repo: PremissaRepository = Depends(get_premissa_repository),
) -> ObterPremissaAtivaUseCase:
    return ObterPremissaAtivaUseCase(repo)


def get_atualizar_premissa_use_case(
    repo: PremissaRepository = Depends(get_premissa_repository),
) -> AtualizarPremissaUseCase:
    return AtualizarPremissaUseCase(repo)
