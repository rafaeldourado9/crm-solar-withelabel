from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.config import settings
from src.database import get_db
from src.deslocamento.application.use_cases import CalcularDeslocamentoUseCase
from src.deslocamento.domain.ports import DistanceProvider
from src.deslocamento.infrastructure.fallback_adapter import FallbackDistanceAdapter
from src.deslocamento.infrastructure.google_maps_adapter import GoogleMapsDistanceAdapter
from src.premissas.domain.repositories import PremissaRepository
from src.premissas.infrastructure.repositories import SQLAlchemyPremissaRepository


def get_distance_provider() -> DistanceProvider:
    if settings.google_maps_api_key:
        return GoogleMapsDistanceAdapter()
    return FallbackDistanceAdapter()


def get_premissa_repository_for_deslocamento(
    db: AsyncSession = Depends(get_db),
) -> PremissaRepository:
    return SQLAlchemyPremissaRepository(db)


def get_calcular_deslocamento_use_case(
    premissa_repo: PremissaRepository = Depends(get_premissa_repository_for_deslocamento),
    distance_provider: DistanceProvider = Depends(get_distance_provider),
) -> CalcularDeslocamentoUseCase:
    return CalcularDeslocamentoUseCase(premissa_repo, distance_provider)
