from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_db
from src.vendedores.infrastructure.repositories import SQLAlchemyVendaVendedorRepository


def get_venda_vendedor_repository(
    db: AsyncSession = Depends(get_db),
) -> SQLAlchemyVendaVendedorRepository:
    return SQLAlchemyVendaVendedorRepository(db)
