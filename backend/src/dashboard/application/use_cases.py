"""Dashboard: agregações multi-repo com cache Redis opcional."""
import json
from datetime import datetime, timedelta
from decimal import Decimal
from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.infrastructure.models import UserModel
from src.clientes.infrastructure.models import ClienteModel
from src.contratos.infrastructure.models import ContratoModel
from src.dashboard.application.dtos import (
    DashboardResponse,
    TopVendedor,
    UltimoCliente,
)
from src.premissas.infrastructure.repositories import SQLAlchemyPremissaRepository
from src.propostas.infrastructure.models import PropostaModel

_CACHE_KEY = "dashboard:resumo:{tenant_id}"
_CACHE_TTL = 300  # 5 minutos


class DashboardResumoUseCase:
    def __init__(self, session: AsyncSession, redis=None):
        self.session = session
        self.redis = redis
        self.premissa_repo = SQLAlchemyPremissaRepository(session)

    async def execute(self, tenant_id: UUID) -> DashboardResponse:
        # Tenta cache Redis
        if self.redis:
            cached = await self._get_cache(tenant_id)
            if cached:
                return DashboardResponse(**cached)

        data = await self._query(tenant_id)

        if self.redis:
            await self._set_cache(tenant_id, data)

        return data

    async def _query(self, tenant_id: UUID) -> DashboardResponse:
        agora = datetime.utcnow()
        inicio_mes = agora.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        trinta_dias = agora - timedelta(days=30)

        # Total clientes
        r = await self.session.execute(
            select(func.count(ClienteModel.id)).where(ClienteModel.tenant_id == tenant_id)
        )
        total_clientes = r.scalar_one()

        # Leads 30d
        r = await self.session.execute(
            select(func.count(ClienteModel.id)).where(
                ClienteModel.tenant_id == tenant_id,
                ClienteModel.created_at >= trinta_dias,
            )
        )
        leads_30d = r.scalar_one()

        # Propostas ativas (pendente)
        r = await self.session.execute(
            select(func.count(PropostaModel.id)).where(
                PropostaModel.tenant_id == tenant_id,
                PropostaModel.status == "pendente",
            )
        )
        propostas_ativas = r.scalar_one()

        # Contratos do mês + faturamento
        r = await self.session.execute(
            select(
                func.count(ContratoModel.id),
                func.coalesce(func.sum(ContratoModel.valor_total), 0),
            ).where(
                ContratoModel.tenant_id == tenant_id,
                ContratoModel.created_at >= inicio_mes,
            )
        )
        contratos_mes, faturamento_mensal = r.one()
        faturamento_mensal = Decimal(str(faturamento_mensal))

        # Comissões pendentes (premissa × faturamento_mensal)
        premissa = await self.premissa_repo.get_ativa(tenant_id)
        comissao_pct = Decimal(str(premissa.comissao_percentual)) if premissa else Decimal("5")
        comissoes_pendentes = (faturamento_mensal * comissao_pct / 100).quantize(Decimal("0.01"))

        # Top 5 vendedores (todos os tempos)
        r = await self.session.execute(
            select(
                ContratoModel.vendedor_id,
                UserModel.nome,
                func.count(ContratoModel.id).label("total"),
                func.coalesce(func.sum(ContratoModel.valor_total), 0).label("valor"),
            )
            .join(UserModel, UserModel.id == ContratoModel.vendedor_id, isouter=True)
            .where(ContratoModel.tenant_id == tenant_id)
            .group_by(ContratoModel.vendedor_id, UserModel.nome)
            .order_by(func.count(ContratoModel.id).desc())
            .limit(5)
        )
        top_vendedores = [
            TopVendedor(
                vendedor_id=row.vendedor_id,
                nome=row.nome or "—",
                total_contratos=row.total,
                valor_total=Decimal(str(row.valor)),
            )
            for row in r.all()
            if row.vendedor_id is not None
        ]

        # Últimos 5 clientes
        r = await self.session.execute(
            select(ClienteModel)
            .where(ClienteModel.tenant_id == tenant_id)
            .order_by(ClienteModel.created_at.desc())
            .limit(5)
        )
        ultimos_clientes = [
            UltimoCliente(
                id=m.id,
                nome=m.nome,
                telefone=m.telefone,
                status=m.status,
                created_at=m.created_at.isoformat(),
            )
            for m in r.scalars().all()
        ]

        return DashboardResponse(
            total_clientes=total_clientes,
            leads_30d=leads_30d,
            propostas_ativas=propostas_ativas,
            contratos_mes=contratos_mes,
            faturamento_mensal=faturamento_mensal,
            comissoes_pendentes=comissoes_pendentes,
            top_vendedores=top_vendedores,
            ultimos_clientes=ultimos_clientes,
        )

    async def _get_cache(self, tenant_id: UUID) -> dict | None:
        try:
            key = _CACHE_KEY.format(tenant_id=tenant_id)
            raw = await self.redis.get(key)
            return json.loads(raw) if raw else None
        except Exception:
            return None

    async def _set_cache(self, tenant_id: UUID, data: DashboardResponse) -> None:
        try:
            key = _CACHE_KEY.format(tenant_id=tenant_id)
            await self.redis.setex(key, _CACHE_TTL, data.model_dump_json())
        except Exception:
            pass
