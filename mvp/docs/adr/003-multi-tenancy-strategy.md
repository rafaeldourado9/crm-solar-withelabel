# ADR-003: Estrategia de Multi-Tenancy

## Status
Aceita

## Contexto
Projeto atual e single-tenant com dados da MAB Energia Solar hardcoded.
Para ser SaaS WhiteLabel, precisa de isolamento total entre tenants.

## Opcoes Consideradas

1. **Schema por tenant** (PostgreSQL schemas) - Isolamento forte, complexo de gerenciar
2. **Database por tenant** - Maximo isolamento, custo alto
3. **Row-level isolation** (tenant_id em toda tabela) - Simples, escalavel

## Decisao
Row-level isolation com `tenant_id` em todas as tabelas.

## Implementacao

```python
# Toda entidade tem tenant_id
class TenantMixin:
    tenant_id: UUID  # FK para tenants.id, indexado

# Middleware extrai tenant do JWT
# Repository sempre filtra por tenant_id
# Impossivel acessar dados de outro tenant
```

## Consequencias

### Positivas
- Simples de implementar e manter
- Um banco para todos os tenants (custo baixo)
- Migrações unificadas
- Queries com indice no tenant_id sao rapidas

### Negativas
- Bug no filtro pode vazar dados (mitigado por testes e middleware)
- Tenant grande pode impactar performance dos menores

### Mitigacao
- Testes automaticos verificam isolamento
- Indice composto (tenant_id, id) em toda tabela
- Rate limiting por tenant
