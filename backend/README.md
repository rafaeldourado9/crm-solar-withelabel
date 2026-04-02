# SunOps SaaS - MVP Backend

Plataforma SaaS WhiteLabel para empresas de energia solar.

## 🚀 Sprint 01 - COMPLETA ✅

### Módulos Implementados

- ✅ **Tenant** - Multi-tenancy com branding customizado
- ✅ **Auth** - JWT authentication (access + refresh tokens)
- ✅ **Premissas** - Configurações de negócio por tenant
- ✅ **Equipamentos** - Painéis e inversores com validação

### Tecnologias

- Python 3.12+
- FastAPI 0.109+
- SQLAlchemy 2.0 (async)
- PostgreSQL 15
- Redis 7
- Alembic (migrations)
- pytest + pytest-asyncio

## 📦 Instalação

### 1. Instalar dependências

```bash
cd backend
pip install -e ".[dev]"
```

### 2. Configurar ambiente

```bash
cp .env.example .env
# Editar .env com suas configurações
```

### 3. Rodar com Docker Compose

```bash
cd ..
docker-compose up -d
```

A API estará disponível em: http://localhost:8000

### 4. Rodar migrations

```bash
cd backend
alembic upgrade head
```

## 🧪 Testes

```bash
# Todos os testes
pytest

# Com cobertura
pytest --cov=src --cov-report=html

# Apenas um módulo
pytest src/tenant/tests/ -v
```

## 📚 Documentação da API

Acesse: http://localhost:8000/docs

## 🏗️ Arquitetura

Arquitetura Hexagonal (Ports & Adapters) com:

```
modulo/
  domain/          # Entidades e lógica de negócio pura
  application/     # Use cases e DTOs
  infrastructure/  # Adapters (DB, API, etc)
  tests/          # Testes unitários e integração
```

## 📋 Endpoints Principais

### Auth
- `POST /api/v1/auth/login` - Login
- `POST /api/v1/auth/refresh` - Renovar token
- `GET /api/v1/auth/me` - Dados do usuário

### Tenants
- `POST /api/v1/tenants` - Criar tenant
- `GET /api/v1/tenants/{id}` - Obter tenant
- `PUT /api/v1/tenants/{id}` - Atualizar tenant

### Premissas
- `GET /api/v1/premissas/ativa` - Obter premissas ativas
- `PUT /api/v1/premissas/{id}` - Atualizar premissas

### Equipamentos
- `GET /api/v1/paineis` - Listar painéis
- `POST /api/v1/paineis` - Criar painel
- `GET /api/v1/inversores` - Listar inversores
- `POST /api/v1/inversores` - Criar inversor
- `POST /api/v1/equipamentos/validar-dimensionamento` - Validar dimensionamento

## 🔄 Próximas Sprints

- **Sprint 02**: Clientes, Orçamentos (core business), Deslocamento
- **Sprint 03**: Propostas, Contratos, Documentos (DOCX/PDF)
- **Sprint 04**: Vendedores, Comissões, Dashboard

## 📖 Documentação Completa

Veja em `docs/`:
- `VISAO_GERAL.md` - Visão geral do projeto
- `ARQUITETURA_HEXAGONAL.md` - Detalhes da arquitetura
- `REGRAS_NEGOCIO.md` - Regras de negócio e cálculos
- `API_ENDPOINTS.md` - Lista completa de endpoints
- `sprints/` - Planejamento das sprints

## 🎯 Métricas de Qualidade

- Cobertura de testes: > 80%
- Complexidade ciclomática: < 5
- Type checking: strict (mypy)
- Linting: ruff

## 📝 Migrations

```bash
# Criar nova migration
alembic revision --autogenerate -m "descricao"

# Aplicar migrations
alembic upgrade head

# Reverter última migration
alembic downgrade -1
```

## 🐛 Debug

```bash
# Rodar API em modo debug
uvicorn src.main:app --reload --log-level debug

# Ver logs do Docker
docker-compose logs -f api
```

## 📄 Licença

Proprietary - MAB Energia Solar
