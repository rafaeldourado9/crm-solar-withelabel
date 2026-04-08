# Estrutura do Projeto - MVP FastAPI

```
mvp/
  docs/                          # Documentacao (este diretorio)
    VISAO_GERAL.md
    ARQUITETURA_HEXAGONAL.md
    REGRAS_NEGOCIO.md
    ESTRUTURA_PROJETO.md
    API_ENDPOINTS.md
    CONTROLE_QUALIDADE.md
    adr/
      001-fastapi-over-django.md
      002-hexagonal-architecture.md
      003-multi-tenancy-strategy.md
      004-jwt-authentication.md
      005-document-generation.md
      006-tdd-quality-control.md
    sprints/
      SPRINT_01_FOUNDATION.md
      SPRINT_02_CORE_BUSINESS.md
      SPRINT_03_DOCUMENTS.md
      SPRINT_04_SALES_DASHBOARD.md

  backend/
    pyproject.toml
    alembic.ini
    alembic/
      env.py
      versions/

    src/
      main.py                    # FastAPI app factory
      config.py                  # Settings (pydantic-settings)
      database.py                # SQLAlchemy async engine + session

      shared/                    # Kernel compartilhado
        __init__.py
        base_entity.py           # BaseEntity(id, created_at, updated_at)
        base_repository.py       # TenantAwareRepository
        base_model.py            # SQLAlchemy base + TenantMixin
        exceptions.py            # DomainError, NotFoundError, etc.
        value_objects.py         # Money, CPF, CNPJ, Email
        utils.py                 # numero_por_extenso, format_brl, etc.

      tenant/
        __init__.py
        domain/
          entities.py            # Tenant(razao_social, cnpj, branding...)
          repositories.py        # TenantRepository(Protocol)
        application/
          use_cases.py           # CriarTenant, AtualizarTenant
          dtos.py
        infrastructure/
          models.py              # TenantModel(SQLAlchemy)
          repositories.py        # SQLAlchemyTenantRepository
          api.py                 # FastAPI router
          dependencies.py

      auth/
        __init__.py
        domain/
          entities.py            # User(email, role, tenant_id)
          services.py            # JWTService, PasswordService
          repositories.py        # UserRepository(Protocol)
        application/
          use_cases.py           # Login, Refresh, Logout
          dtos.py
        infrastructure/
          models.py
          repositories.py
          api.py
          dependencies.py        # get_current_user, get_current_tenant
          middleware.py           # TenantMiddleware

      clientes/
        __init__.py
        domain/
          entities.py            # Cliente(nome, cpf_cnpj, status...)
          repositories.py
        application/
          use_cases.py
          dtos.py
        infrastructure/
          models.py
          repositories.py
          api.py
          dependencies.py
        tests/

      equipamentos/
        __init__.py
        domain/
          entities.py            # Painel, Inversor
          services.py            # ValidacaoDimensionamento
          repositories.py
        application/
          use_cases.py
          dtos.py
        infrastructure/
          models.py
          repositories.py
          api.py
          dependencies.py
        tests/

      premissas/
        __init__.py
        domain/
          entities.py            # Premissa (singleton por tenant)
          repositories.py
        application/
          use_cases.py
          dtos.py
        infrastructure/
          models.py
          repositories.py
          api.py
          dependencies.py
        tests/

      orcamentos/
        __init__.py
        domain/
          entities.py            # Orcamento, Dimensionamento
          value_objects.py       # CustoBreakdown, MargemConfig, FormaPagamento
          services.py            # SolarCalculatorService (logica pura)
          repositories.py
          exceptions.py
        application/
          use_cases.py           # CriarOrcamento, ValidarDimensionamento, etc.
          dtos.py
        infrastructure/
          models.py
          repositories.py
          api.py
          dependencies.py
        tests/
          test_domain.py         # Testes do SolarCalculator
          test_use_cases.py
          test_api.py

      deslocamento/
        __init__.py
        domain/
          services.py            # DeslocamentoCalculator (logica pura)
          ports.py               # DistanceProvider(Protocol)
        application/
          use_cases.py
          dtos.py
        infrastructure/
          google_maps_adapter.py # Adapter async para Google Maps
          fallback_adapter.py    # Tabela de distancias
          api.py
          dependencies.py
        tests/

      propostas/
        __init__.py
        domain/
          entities.py            # Proposta(status: pendente/aceita/recusada)
          repositories.py
        application/
          use_cases.py           # CriarProposta, AceitarProposta
          dtos.py
        infrastructure/
          models.py
          repositories.py
          api.py
          dependencies.py
        tests/

      contratos/
        __init__.py
        domain/
          entities.py            # Contrato (dados empresa do TENANT)
          repositories.py
        application/
          use_cases.py           # CriarContrato, GerarDocx, GerarPdf
          dtos.py
        infrastructure/
          models.py
          repositories.py
          api.py
          dependencies.py
        tests/

      documentos/
        __init__.py
        domain/
          services.py            # TemplateEngine (substituicao variaveis)
          ports.py               # DocxRenderer, PdfRenderer (Protocol)
        application/
          use_cases.py           # GerarDocumento
          dtos.py
        infrastructure/
          docx_adapter.py        # python-docx implementation
          pdf_adapter.py         # WeasyPrint implementation
          api.py
          dependencies.py
        tests/
          test_template_engine.py

      vendedores/
        __init__.py
        domain/
          entities.py            # Vendedor, VendaVendedor
          services.py            # ComissaoCalculator
          repositories.py
        application/
          use_cases.py
          dtos.py
        infrastructure/
          models.py
          repositories.py
          api.py
          dependencies.py
        tests/

      dashboard/
        __init__.py
        application/
          use_cases.py           # DashboardResumo
          dtos.py
        infrastructure/
          api.py
          dependencies.py

    tests/
      conftest.py                # Fixtures globais (db, client, tenant)
      test_health.py

  docker-compose.yml
  Dockerfile
  .env.example

frontend/                        # REAPROVEITADO do projeto atual
  src/
    services/api.js              # Atualizar endpoints + JWT auth
    pages/                       # Manter como esta
    components/                  # Manter como esta
```

## Convencoes

### Nomes de Arquivo
- `entities.py` - Entidades de dominio (dataclass/pydantic)
- `services.py` - Logica de negocio pura
- `repositories.py` - Em domain: Protocol. Em infra: implementacao
- `use_cases.py` - Orquestracao de operacoes
- `dtos.py` - Data Transfer Objects (request/response schemas)
- `api.py` - FastAPI routers
- `models.py` - SQLAlchemy models
- `dependencies.py` - FastAPI Depends() factories

### Nomes de Classe
- Entities: `Cliente`, `Orcamento` (substantivo)
- Services: `SolarCalculatorService`, `ComissaoCalculator` (verbo + substantivo)
- Use Cases: `CriarOrcamento`, `AceitarProposta` (verbo no infinitivo)
- Repositories: `ClienteRepository` (Protocol), `SQLAlchemyClienteRepository` (impl)
- DTOs: `CriarOrcamentoDTO`, `OrcamentoResponseDTO`
