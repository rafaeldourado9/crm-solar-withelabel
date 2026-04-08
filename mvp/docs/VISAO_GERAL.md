# SunOps SaaS - MVP Vision

## O que e o SunOps?

Plataforma SaaS WhiteLabel para empresas de energia solar gerenciarem:
- Clientes e vendedores
- Orcamentos com calculo automatico (dimensionamento solar)
- Propostas comerciais
- Contratos com geracao DOCX/PDF
- Comissoes de vendedores
- Dashboard analitico

## Problema atual (Django)

| Problema | Impacto |
|----------|---------|
| Orcamentos nao sao criados corretamente | Core quebrado |
| Variaveis DOCX nao carregam nos templates | Documentos invalidos |
| Contratos nao sao gerados | Fluxo comercial bloqueado |
| Dados da empresa hardcoded (MAB Energia) | Impossibilita WhiteLabel |
| Auth sem expiracao de token | Vulnerabilidade de seguranca |
| Calculo deslocamento retorna 501 | Feature morta |
| PDF depende de LibreOffice subprocess | Gargalo e fragilidade |

## Solucao: FastAPI + Arquitetura Hexagonal

### Principios

1. **Bounded Contexts** - Cada modulo isolado com dominio proprio
2. **Hexagonal Architecture** - Ports & Adapters (dominio independente de framework)
3. **TDD** - Testes primeiro, codigo depois
4. **CC baixa** - Complexidade ciclomatica < 5 por funcao
5. **Async-first** - FastAPI com async/await nativo
6. **Multi-tenant** - Isolamento total por tenant (WhiteLabel)
7. **SaaS-ready** - Billing, branding, planos por tenant

### Stack MVP

| Camada | Tecnologia |
|--------|-----------|
| API | FastAPI 0.109+ (async) |
| ORM | SQLAlchemy 2.0 + Alembic |
| DB | PostgreSQL 15 |
| Cache | Redis 7 |
| Auth | JWT (access + refresh tokens) |
| Tasks | Celery 5.4 / ARQ (async) |
| DOCX | python-docx |
| PDF | WeasyPrint (sem LibreOffice) |
| Testes | pytest + pytest-asyncio |
| Frontend | React 18.2 (reaproveitado) |

## Bounded Contexts (Modulos)

```
mvp/backend/
  src/
    tenant/          # Multi-tenancy, branding, planos
    auth/            # JWT, usuarios, permissoes
    clientes/        # Gestao de clientes
    equipamentos/    # Paineis, inversores, catalogo
    premissas/       # Regras de negocio configuráveis
    orcamentos/      # Calculo solar, dimensionamento, pricing
    propostas/       # Propostas comerciais
    contratos/       # Contratos, geracao DOCX/PDF
    vendedores/      # Equipe comercial, comissoes
    deslocamento/    # Calculo distancia e custo viagem
    documentos/      # Engine de templates DOCX/PDF
    dashboard/       # Analytics e KPIs
    shared/          # Kernel compartilhado (value objects, base classes)
```

## Metricas de Qualidade

- Cobertura de testes: > 80%
- Complexidade ciclomatica: < 5 por funcao
- Tempo de resposta API: < 200ms (p95)
- Zero dados hardcoded de empresa
- 100% das variaveis DOCX mapeadas e testadas
