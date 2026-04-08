# Arquitetura Hexagonal - SunOps SaaS

## Estrutura por Modulo (Bounded Context)

Cada modulo segue a mesma estrutura:

```
modulo/
  __init__.py
  domain/
    __init__.py
    entities.py        # Entidades de dominio (dataclasses/pydantic)
    value_objects.py    # Value Objects imutaveis
    repositories.py    # Port - Interface abstrata do repositorio
    services.py        # Logica de negocio pura (sem dependencias externas)
    exceptions.py      # Excecoes de dominio
  application/
    __init__.py
    use_cases.py       # Orquestracao de casos de uso
    dtos.py            # Data Transfer Objects (entrada/saida)
  infrastructure/
    __init__.py
    models.py          # SQLAlchemy models (Adapter)
    repositories.py    # Implementacao concreta do repositorio (Adapter)
    api.py             # FastAPI router (Adapter)
    dependencies.py    # Dependency injection
  tests/
    __init__.py
    test_domain.py     # Testes unitarios do dominio
    test_use_cases.py  # Testes de integracao
    test_api.py        # Testes E2E da API
    conftest.py        # Fixtures
```

## Camadas

```
                    ┌─────────────────────────────┐
                    │      API (FastAPI Router)    │  ← Adapter (entrada)
                    └──────────────┬──────────────┘
                                   │
                    ┌──────────────▼──────────────┐
                    │     Application Layer        │  ← Use Cases / DTOs
                    │     (orquestracao)            │
                    └──────────────┬──────────────┘
                                   │
                    ┌──────────────▼──────────────┐
                    │      Domain Layer            │  ← Entities / Services
                    │   (regras de negocio puras)   │     (SEM dependencias)
                    └──────────────┬──────────────┘
                                   │
                    ┌──────────────▼──────────────┐
                    │   Infrastructure Layer        │  ← Adapters (saida)
                    │  (DB, Cache, APIs externas)   │
                    └─────────────────────────────┘
```

## Regras

1. **Domain NAO importa nada de infrastructure** - Zero dependencia de SQLAlchemy, FastAPI, Redis
2. **Application orquestra** - Chama domain services, usa ports para persistencia
3. **Infrastructure implementa ports** - Repositorios concretos, API routers
4. **Dependency Injection** - FastAPI `Depends()` injeta adapters nos use cases

## Exemplo: Modulo Orcamentos

```python
# domain/entities.py
@dataclass
class Orcamento:
    id: UUID
    tenant_id: UUID
    cliente_id: UUID
    paineis: list[PainelConfig]
    inversor: InversorConfig
    custos: CustoBreakdown
    margem: MargemConfig
    forma_pagamento: FormaPagamento
    status: OrcamentoStatus

    def calcular_valor_final(self) -> Decimal:
        """Logica pura de calculo - testavel sem banco"""
        subtotal = self.custos.total()
        markup = self._aplicar_margens(subtotal, self.margem)
        return self._arredondar_centena(markup)

# domain/repositories.py (Port)
class OrcamentoRepository(Protocol):
    async def save(self, orcamento: Orcamento) -> Orcamento: ...
    async def find_by_id(self, id: UUID, tenant_id: UUID) -> Orcamento | None: ...

# domain/services.py
class SolarCalculatorService:
    """Sem dependencias externas - logica pura"""
    def dimensionar(self, consumo_mensal: Decimal, painel: PainelConfig,
                    hsp: Decimal, perda: Decimal) -> Dimensionamento:
        potencia_necessaria = consumo_mensal / (hsp * 30 * (1 - perda))
        qtd_paineis = ceil(potencia_necessaria * 1000 / painel.potencia_w)
        ...

# application/use_cases.py
class CriarOrcamentoUseCase:
    def __init__(self, repo: OrcamentoRepository, premissa_repo: PremissaRepository):
        self.repo = repo
        self.premissa_repo = premissa_repo

    async def execute(self, dto: CriarOrcamentoDTO) -> OrcamentoResponseDTO:
        premissas = await self.premissa_repo.get_ativa(dto.tenant_id)
        orcamento = SolarCalculatorService.calcular(dto, premissas)
        saved = await self.repo.save(orcamento)
        return OrcamentoResponseDTO.from_entity(saved)

# infrastructure/api.py (Adapter)
router = APIRouter(prefix="/orcamentos", tags=["orcamentos"])

@router.post("/", response_model=OrcamentoResponse)
async def criar_orcamento(
    dto: CriarOrcamentoRequest,
    use_case: CriarOrcamentoUseCase = Depends(get_criar_orcamento_use_case),
    tenant: Tenant = Depends(get_current_tenant),
):
    return await use_case.execute(dto.to_dto(tenant.id))
```

## Multi-Tenancy

```python
# shared/tenant.py
class TenantMixin:
    """Mixin para todos os models SQLAlchemy"""
    tenant_id: Mapped[UUID] = mapped_column(ForeignKey("tenants.id"), index=True)

# shared/middleware.py
class TenantMiddleware:
    """Extrai tenant do JWT ou subdomain"""
    async def __call__(self, request, call_next):
        tenant = extract_tenant(request)
        request.state.tenant = tenant
        return await call_next(request)
```

## Dependency Injection

```python
# infrastructure/dependencies.py
def get_orcamento_repository(db: AsyncSession = Depends(get_db)) -> OrcamentoRepository:
    return SQLAlchemyOrcamentoRepository(db)

def get_criar_orcamento_use_case(
    repo: OrcamentoRepository = Depends(get_orcamento_repository),
    premissa_repo: PremissaRepository = Depends(get_premissa_repository),
) -> CriarOrcamentoUseCase:
    return CriarOrcamentoUseCase(repo, premissa_repo)
```
