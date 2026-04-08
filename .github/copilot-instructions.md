# SunOps — Project Guidelines

SunOps is a Brazilian solar energy SaaS (CRM/ERP) for managing customers, quotes, proposals, and contracts. Internal codebase name is `crm_solar`. All domain names, model fields, endpoints, and docs are in **Brazilian Portuguese**.

## Architecture

3-tier: React SPA → Nginx → Django REST API → PostgreSQL + Redis (Celery async tasks).

- **Backend pattern**: `View → Service → Model`. Business logic lives in service classes, **not** in views.
  - Key example: `backend/apps/orcamentos/services.py` — `SolarCalculator` class orchestrates all solar engineering calculations.
- **Singleton Premissa**: system-wide config uses `Premissa.get_ativa()` — only one active record at a time.
- **Hybrid calculation**: server-side is source of truth; client-side mirrors it for immediate feedback.
- See [docs/ARCHITECTURE.md](../docs/ARCHITECTURE.md) for full design decisions.

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python · Django 5 · Django REST Framework 3.14 |
| Frontend | React 18 · Vite 5 · Tailwind CSS 3 · Axios |
| DB | PostgreSQL 15 (ORM: Django migrations — primary) |
| Migrations | Django ORM (primary) + Alembic/SQLAlchemy (secondary — do not mix) |
| Async | Celery 5 + Redis 7 |
| Auth | DRF Token Auth — `POST /api/auth/login/` → `Authorization: Token <token>` |
| AI | Multi-provider: OpenAI, Anthropic, Google Generative AI (`apps/ia_service.py`) |
| Docs | `python-docx`, `docx2pdf`, `reportlab` |
| Infra | Docker Compose · Nginx · Gunicorn |

## Build & Run

```bash
# Full stack (dev)
docker compose up

# Frontend only
cd frontend && npm run dev        # port 5173

# Backend only
cd backend && python manage.py runserver 0.0.0.0:8000

# Production
docker compose -f docker-compose.prod.yml up

# DB migrations (Django ORM — always use this)
python manage.py migrate

# Alembic (secondary — only for SQLAlchemy-specific paths)
scripts/alembic-upgrade.bat
```

See [docs/DOCKER.md](../docs/DOCKER.md) and [docs/DEPLOY.md](../docs/DEPLOY.md) for deployment details.

## Key Backend Apps (`backend/apps/`)

| App | Domain |
|-----|--------|
| `clientes/` | Customer management |
| `vendedores/` | Sales reps |
| `premissas/` | System-wide solar config (HSP, losses, margins) |
| `equipamentos/` | Solar panels & inverters catalog |
| `orcamentos/` | Quotes + `SolarCalculator` |
| `propostas/` | Commercial proposals |
| `contratos/` | Contract generation (DOCX/PDF) |
| `templates/` | Document template management |
| `dashboard/` | KPI endpoints |
| `suporte/` | Support module |

## Conventions

- **Portuguese throughout**: models, serializers, URL names, and variables use PT-BR. Match existing naming — don't translate to English.
- **Service layer**: new business logic goes in a `services.py` file within the app, consumed by views via `get_object_or_404` + service calls.
- **Env vars**: use `python-decouple` (`config('VAR', default=...)`). Never hardcode secrets. No `.env` file is committed.
- **Dual migration system**: Django migrations are authoritative. Alembic is a secondary toolchain — do not create Alembic migrations for Django model changes.
- **Frontend services**: API calls go through `frontend/src/services/` (Axios wrappers), never inline in components.
- **Token auth on all endpoints**: every API request (except `/health/` and `/api/auth/login/`) requires `Authorization: Token <token>`.

## Security

- See [docs/SECURITY_OWASP.md](../docs/SECURITY_OWASP.md) for OWASP compliance notes.
- `django-csp`, `django-ratelimit`, `django-defender` are active — do not disable them.
- Never log or expose `SECRET_KEY`, DB credentials, or auth tokens.

## Key Docs to Consult

| Topic | File |
|-------|------|
| Solar calculation formulas | [docs/CALCULOS.md](../docs/CALCULOS.md) |
| Full REST API reference | [docs/API.md](../docs/API.md) |
| Quote generation flow | [docs/GERACAO_ORCAMENTO.md](../docs/GERACAO_ORCAMENTO.md) |
| Template variables (proposals) | [docs/TEMPLATE_PROPOSTA_COMERCIAL.md](../docs/TEMPLATE_PROPOSTA_COMERCIAL.md) |
| Auto-template system | [docs/SISTEMA_AUTOMATICO_TEMPLATES.md](../docs/SISTEMA_AUTOMATICO_TEMPLATES.md) |
| AWS deployment | [docs/DEPLOY_AWS.md](../docs/DEPLOY_AWS.md) |
