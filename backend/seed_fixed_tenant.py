"""Script para criar um tenant com ID fixo e usuario admin inicial."""
import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from uuid import UUID
from sqlalchemy import select
from src.database import async_session_factory, engine, Base
from src.tenant.infrastructure.models import TenantModel
from src.auth.infrastructure.repositories import SQLAlchemyUserRepository
from src.auth.domain.services import PasswordService
from src.auth.domain.entities import User


async def seed():
    async with async_session_factory() as db:
        # ID fixo esperado pelo frontend
        tenant_id = UUID("a9664639-f0ff-4c9f-ba72-27286841aa69")
        
        # Verificar se já existe este tenant
        result = await db.execute(select(TenantModel).where(TenantModel.id == tenant_id))
        existing_tenant = result.scalar_one_or_none()

        if existing_tenant:
            print(f"Ja existe tenant: {existing_tenant.nome_fantasia} (id={existing_tenant.id})")
        else:
            # Criar tenant com ID fixo
            tenant_data = {
                "id": tenant_id,
                "nome_fantasia": "Empresa Demo",
                "razao_social": "Empresa Demo LTDA",
                "cnpj": "11.111.111/0001-11",
                "endereco": "Rua Demo, 123",
                "cidade": "Sao Paulo",
                "estado": "SP",
                "cep": "01000-000",
                "representante_nome": "Administrador",
                "representante_cpf": "111.111.111-11",
                "plano": "free",
                "ativo": True,
            }
            tenant_model = TenantModel(**tenant_data)
            db.add(tenant_model)
            await db.commit()
            await db.refresh(tenant_model)
            print(f"Tenant criado: {tenant_model.nome_fantasia} (id={tenant_model.id})")

        # Verificar se já existe admin neste tenant
        user_repo = SQLAlchemyUserRepository(db)
        existing_admins = await user_repo.list_by_tenant(tenant_id, roles=["admin"])
        if existing_admins:
            print(f"Ja existem {len(existing_admins)} admin(s) neste tenant. Pulando.")
        else:
            admin = User(
                tenant_id=tenant_id,
                email="admin@sunops.com",
                hashed_password=PasswordService.hash_password("admin123"),
                nome="Administrador",
                role="admin",
            )
            admin = await user_repo.create(admin)
            await db.commit()
            print(f"Admin criado: {admin.email} / senha: admin123")

        print("\n=== Credenciais ===")
        print(f"Email: admin@sunops.com")
        print(f"Senha: admin123")
        print(f"Tenant ID: {tenant_id}")
        print("===================")


if __name__ == "__main__":
    asyncio.run(seed())
