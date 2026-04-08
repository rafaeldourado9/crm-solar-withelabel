from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.domain.entities import User
from src.auth.infrastructure.dependencies import get_current_tenant, get_current_user
from src.config import settings
from src.dashboard.application.dtos import DashboardResponse
from src.dashboard.application.use_cases import DashboardResumoUseCase
from src.database import get_db
from src.tenant.domain.entities import Tenant

router = APIRouter(prefix="/api/v1/dashboard", tags=["dashboard"])


async def _get_redis():
    """Retorna cliente Redis ou None se não disponível."""
    try:
        import redis.asyncio as aioredis
        client = aioredis.from_url(settings.redis_url, decode_responses=True)
        await client.ping()
        return client
    except Exception:
        return None


@router.get("/resumo", response_model=DashboardResponse)
async def dashboard_resumo(
    tenant: Tenant = Depends(get_current_tenant),
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> DashboardResponse:
    redis = await _get_redis()
    return await DashboardResumoUseCase(db, redis).execute(tenant.id)
