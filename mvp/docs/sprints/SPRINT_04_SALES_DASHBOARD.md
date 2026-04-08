# Sprint 04 - Vendedores + Dashboard

**Objetivo**: Gestao comercial e analytics.

**Depende de**: Sprint 03 completa.

---

## Tasks

### 4.1 Modulo Vendedores
- [x] Domain: entidade Vendedor (user, tipo, bloqueado, comissao)
- [x] Domain: entidade VendaVendedor (contrato, valor_venda, valor_comissao, pago)
- [x] Domain: calculo de comissao automatico
- [x] Infrastructure: models + migrations
- [x] Application: CRUD + ResetarSenha + Bloquear + Resumo + HistoricoVendas
- [x] API: endpoints completos

**Criterio**: Vendedor criado, comissao calculada automaticamente ao fechar contrato.

### 4.2 Modulo Dashboard
- [x] Application: DashboardResumo use case
  - total_clientes, leads_30d, propostas_ativas, contratos_mes
  - faturamento_mensal, comissoes_pendentes
  - top_vendedores
- [x] API: GET /dashboard/resumo/
- [x] Cache: Redis 5min para queries pesadas

**Criterio**: Dashboard retorna dados corretos filtrados por tenant.

### 4.3 Integracao Frontend Final
- [x] Dashboard.jsx com dados reais
- [x] Vendedores.jsx funcional
- [x] Branding dinamico por tenant (logo, cores)
- [x] Teste E2E completo de todos os fluxos

**Criterio**: Toda a plataforma funcional no browser com dados reais.

---

## Entregavel
- Gestao completa de vendedores com comissoes
- Dashboard analitico funcional
- Branding WhiteLabel dinamico
- MVP COMPLETO
