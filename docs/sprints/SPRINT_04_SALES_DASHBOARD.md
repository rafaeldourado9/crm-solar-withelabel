# Sprint 04 - Vendedores + Dashboard

**Objetivo**: Gestao comercial e analytics.

**Depende de**: Sprint 03 completa.

---

## Tasks

### 4.1 Modulo Vendedores
- [ ] Domain: entidade Vendedor (user, tipo, bloqueado, comissao)
- [ ] Domain: entidade VendaVendedor (contrato, valor_venda, valor_comissao, pago)
- [ ] Domain: calculo de comissao automatico
- [ ] Infrastructure: models + migrations
- [ ] Application: CRUD + ResetarSenha + Bloquear + Resumo + HistoricoVendas
- [ ] API: endpoints completos

**Criterio**: Vendedor criado, comissao calculada automaticamente ao fechar contrato.

### 4.2 Modulo Dashboard
- [ ] Application: DashboardResumo use case
  - total_clientes, leads_30d, propostas_ativas, contratos_mes
  - faturamento_mensal, comissoes_pendentes
  - top_vendedores
- [ ] API: GET /dashboard/resumo/
- [ ] Cache: Redis 5min para queries pesadas

**Criterio**: Dashboard retorna dados corretos filtrados por tenant.

### 4.3 Integracao Frontend Final
- [ ] Dashboard.jsx com dados reais
- [ ] Vendedores.jsx funcional
- [ ] Branding dinamico por tenant (logo, cores)
- [ ] Teste E2E completo de todos os fluxos

**Criterio**: Toda a plataforma funcional no browser com dados reais.

---

## Entregavel
- Gestao completa de vendedores com comissoes
- Dashboard analitico funcional
- Branding WhiteLabel dinamico
- MVP COMPLETO
