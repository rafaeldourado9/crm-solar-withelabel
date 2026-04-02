# Sprint 01 - Foundation (Infraestrutura + Core)

**Objetivo**: Estrutura base do projeto FastAPI com multi-tenancy, auth e modulos core funcionando.

**Prioridade**: CRITICA - Bloqueia todas as outras sprints.

---

## Tasks

### 1.1 Setup do Projeto FastAPI
- [x] Criar estrutura de pastas (hexagonal por modulo)
- [x] Configurar `pyproject.toml` com dependencias
- [x] Configurar SQLAlchemy 2.0 async + Alembic
- [x] Configurar pytest + pytest-asyncio
- [x] Configurar ruff + mypy
- [x] Docker Compose (postgres, redis, api)
- [x] `.env.example` com todas as variaveis

**Criterio**: `pytest` roda, `docker compose up` sobe, API responde health check.

### 1.2 Shared Kernel
- [x] Base entity com id (UUID), created_at, updated_at
- [x] TenantMixin (tenant_id em toda entidade)
- [x] Database session manager (async)
- [x] Base repository com filtro automatico por tenant
- [x] Exception handlers globais
- [x] Pydantic base schemas

**Criterio**: Testes unitarios passam para base classes.

### 1.3 Modulo Tenant
- [x] Domain: entidade Tenant (razao_social, cnpj, branding, dados bancarios)
- [x] Infrastructure: model SQLAlchemy + migration
- [x] Application: CRUD use cases
- [x] API: endpoints `/tenants/`
- [x] Seed: tenant padrao para dev

**Criterio**: POST/GET /tenants/ funciona. Tenant persiste no banco.

### 1.4 Modulo Auth
- [x] Domain: entidade User (email, hashed_password, role, tenant_id)
- [x] JWT service (access 15min + refresh 7d)
- [x] API: POST /auth/login, POST /auth/refresh, GET /auth/me
- [x] Middleware: extrai tenant + user do JWT
- [x] Dependency: `get_current_user`, `get_current_tenant`
- [x] Redis blacklist para refresh tokens (estrutura pronta)

**Criterio**: Login retorna JWT. Endpoints protegidos rejeitam sem token. Refresh funciona.

### 1.5 Modulo Premissas
- [x] Domain: entidade Premissa com todos os campos (margens, taxas, parametros tecnicos)
- [x] Domain: validacoes (percentuais 0-100, valores positivos)
- [x] Infrastructure: model + migration
- [x] Application: GetPremissaAtiva, UpdatePremissa use cases
- [x] API: GET /premissas/ativa/, PUT /premissas/{id}/
- [x] Seed: premissas default (auto-criadas)

**Criterio**: GET /premissas/ativa/ retorna JSON com todos os campos. Testes cobrem validacoes.

### 1.6 Modulo Equipamentos
- [x] Domain: entidades Painel, Inversor
- [x] Domain: validacao overload (painel vs inversor)
- [x] Infrastructure: models + migrations
- [x] Application: CRUD + validacao dimensionamento
- [x] API: CRUD endpoints + POST /equipamentos/validar-dimensionamento/
- [x] Cache: Redis 15min para listagens (estrutura pronta)

**Criterio**: CRUD funciona. Validacao de dimensionamento retorna correto.

---

## Entregavel
API FastAPI rodando com:
- [x] Auth JWT funcional
- [x] Multi-tenancy com isolamento
- [x] Premissas configuraveis por tenant
- [x] Equipamentos com validacao de dimensionamento
- [x] Testes unitarios e de integracao passando (dominio)
- [x] Docker compose subindo tudo
- [x] Migrations Alembic (001-004)
