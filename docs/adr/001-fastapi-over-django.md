# ADR-001: FastAPI ao inves de Django

## Status
Aceita

## Contexto
O backend atual usa Django 5.0.1 + DRF. O projeto sofre com:
- Orcamentos nao funcionam (bug no fluxo de criacao)
- Templates DOCX nao substituem variaveis corretamente
- Contratos nao sao gerados
- PDF depende de subprocess LibreOffice (fragil)
- Sem async nativo (Django ORM e sincrono)
- Estrutura monolitica dificulta isolamento

## Decisao
Migrar para FastAPI com SQLAlchemy 2.0 async.

## Consequencias

### Positivas
- Async nativo (I/O nao-bloqueante para Google Maps, IA, etc.)
- Pydantic nativo para validacao (type-safe)
- OpenAPI/Swagger automatico
- Dependency Injection built-in (perfeito para hexagonal)
- Performance 3-5x superior em I/O bound
- Menor footprint de memoria

### Negativas
- Perda do Django Admin (substituir por painel custom no frontend)
- Migracao de modelos Django -> SQLAlchemy
- Equipe precisa aprender FastAPI (curva suave)

### Mitigacao
- Frontend React e 100% reaproveitado (mesmos endpoints)
- Logica de calculo solar e pura Python (portavel)
- SQLAlchemy 2.0 tem ORM tao expressivo quanto Django ORM
