from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.clientes.domain.repositories import ClienteRepository
from src.clientes.infrastructure.repositories import SQLAlchemyClienteRepository
from src.database import get_db
from src.equipamentos.domain.repositories import InversorRepository, PainelRepository
from src.equipamentos.infrastructure.repositories import (
    SQLAlchemyInversorRepository,
    SQLAlchemyPainelRepository,
)
from src.orcamentos.application.use_cases import (
    AtualizarOrcamentoUseCase,
    CriarOrcamentoUseCase,
    DeletarOrcamentoUseCase,
    ListarOrcamentosUseCase,
    ObterOrcamentoUseCase,
)
from src.orcamentos.domain.repositories import OrcamentoRepository
from src.orcamentos.infrastructure.repositories import SQLAlchemyOrcamentoRepository
from src.premissas.domain.repositories import PremissaRepository
from src.premissas.infrastructure.repositories import SQLAlchemyPremissaRepository


def get_orcamento_repository(db: AsyncSession = Depends(get_db)) -> OrcamentoRepository:
    return SQLAlchemyOrcamentoRepository(db)


def get_criar_orcamento_use_case(
    db: AsyncSession = Depends(get_db),
) -> CriarOrcamentoUseCase:
    return CriarOrcamentoUseCase(
        orcamento_repo=SQLAlchemyOrcamentoRepository(db),
        premissa_repo=SQLAlchemyPremissaRepository(db),
        painel_repo=SQLAlchemyPainelRepository(db),
        inversor_repo=SQLAlchemyInversorRepository(db),
        cliente_repo=SQLAlchemyClienteRepository(db),
    )


def get_listar_orcamentos_use_case(
    repo: OrcamentoRepository = Depends(get_orcamento_repository),
) -> ListarOrcamentosUseCase:
    return ListarOrcamentosUseCase(repo)


def get_obter_orcamento_use_case(
    repo: OrcamentoRepository = Depends(get_orcamento_repository),
) -> ObterOrcamentoUseCase:
    return ObterOrcamentoUseCase(repo)


def get_atualizar_orcamento_use_case(
    db: AsyncSession = Depends(get_db),
) -> AtualizarOrcamentoUseCase:
    return AtualizarOrcamentoUseCase(
        orcamento_repo=SQLAlchemyOrcamentoRepository(db),
        premissa_repo=SQLAlchemyPremissaRepository(db),
        painel_repo=SQLAlchemyPainelRepository(db),
        inversor_repo=SQLAlchemyInversorRepository(db),
    )


def get_deletar_orcamento_use_case(
    repo: OrcamentoRepository = Depends(get_orcamento_repository),
) -> DeletarOrcamentoUseCase:
    return DeletarOrcamentoUseCase(repo)
