from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.clientes.infrastructure.repositories import SQLAlchemyClienteRepository
from src.database import get_db
from src.orcamentos.infrastructure.repositories import SQLAlchemyOrcamentoRepository
from src.propostas.application.use_cases import (
    AceitarPropostaUseCase,
    CriarPropostaUseCase,
    ListarPropostasUseCase,
    ObterPropostaUseCase,
    RecusarPropostaUseCase,
)
from src.propostas.infrastructure.repositories import SQLAlchemyPropostaRepository


def get_criar_proposta_use_case(db: AsyncSession = Depends(get_db)) -> CriarPropostaUseCase:
    return CriarPropostaUseCase(
        proposta_repo=SQLAlchemyPropostaRepository(db),
        orcamento_repo=SQLAlchemyOrcamentoRepository(db),
        cliente_repo=SQLAlchemyClienteRepository(db),
    )


def get_listar_propostas_use_case(db: AsyncSession = Depends(get_db)) -> ListarPropostasUseCase:
    return ListarPropostasUseCase(SQLAlchemyPropostaRepository(db))


def get_obter_proposta_use_case(db: AsyncSession = Depends(get_db)) -> ObterPropostaUseCase:
    return ObterPropostaUseCase(SQLAlchemyPropostaRepository(db))


def get_aceitar_proposta_use_case(db: AsyncSession = Depends(get_db)) -> AceitarPropostaUseCase:
    return AceitarPropostaUseCase(SQLAlchemyPropostaRepository(db))


def get_recusar_proposta_use_case(db: AsyncSession = Depends(get_db)) -> RecusarPropostaUseCase:
    return RecusarPropostaUseCase(SQLAlchemyPropostaRepository(db))
