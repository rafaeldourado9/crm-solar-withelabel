# Sprint 02 - Core Business (Orcamentos + Clientes)

**Objetivo**: Fluxo principal funcionando - criar clientes, calcular e gerar orcamentos.

**Depende de**: Sprint 01 completa.

---

## Tasks

### 2.1 Modulo Clientes
- [x] Domain: entidade Cliente (nome, cpf_cnpj, telefone, email, endereco completo, status, vendedor_id)
- [x] Domain: status machine (orcamento -> proposta -> contrato)
- [x] Infrastructure: model + migration (005_create_clientes_table.py)
- [x] Application: CRUD + filtros por vendedor/status
- [x] API: CRUD endpoints com paginacao
- [x] Permissoes: vendedor ve so seus clientes

**Criterio**: CRUD funciona. Vendedor nao ve clientes de outro vendedor.

### 2.2 Modulo Deslocamento
- [x] Domain: service DeslocamentoCalculator (logica pura)
  - Calculo distancia * 2 * consumo * preco * margem
  - Lista de cidades isentas
- [x] Infrastructure: adapter Google Maps API (async httpx)
- [x] Infrastructure: adapter tabela fallback (16 cidades)
- [x] Application: CalcularDeslocamento use case
- [x] API: POST /deslocamento/calcular/
- [x] Testes: com mock da API externa

**Criterio**: Calculo correto para cidades com/sem cobranca. Google Maps fallback funciona.

### 2.3 Modulo Orcamentos - Domain
- [x] Entidade Orcamento com todos os campos (40+ campos)
- [x] Value Objects: CustoBreakdown, MargemConfig, FormaPagamento, Dimensionamento
- [x] SolarCalculatorService (logica pura):
  - dimensionar_tecnico()
  - calcular_subtotal()
  - aplicar_margens()
  - aplicar_juros()
  - calcular_economia_25_anos()
- [x] Testes unitarios para CADA formula

**Criterio**: Todos os calculos batem com os exemplos da doc CALCULOS.md. CC < 5.

### 2.4 Modulo Orcamentos - Application + API
- [x] Use cases: CriarOrcamento, AtualizarOrcamento, ListarOrcamentos
- [x] Use cases: ValidarDimensionamento, CalcularMaterialEletrico
- [x] DTOs de entrada/saida
- [x] API: CRUD + acoes customizadas (+ /calcular-material-eletrico)
- [x] Integracao com Premissas (busca ativa automaticamente)
- [x] Integracao com Deslocamento
- [x] Infrastructure: model + migration (006_create_orcamentos_table.py)

**Criterio**: POST /orcamentos/ cria orcamento com calculo correto. GET lista com paginacao.

### 2.5 Integracao Frontend - Orcamentos
- [x] Mover frontend para mvp/frontend/
- [x] Atualizar `api.js` para novos endpoints FastAPI (/api/v1)
- [x] Ajustar autenticacao para JWT (Bearer ao inves de Token)
- [x] Atualizar Login.jsx para usar email + salvar access_token/refresh_token
- [x] Atualizar PrivateRoute para verificar access_token
- [x] Proxy vite apontando para servico `api` (docker compose)
- [x] Nginx proxy /api/v1/ -> api:8000 (producao)
- [x] Dockerfile.dev para hot-reload em desenvolvimento
- [x] Frontend adicionado ao docker-compose.yml
- [ ] Testar fluxo completo: login -> criar cliente -> criar orcamento (requer ambiente rodando)

**Criterio**: Fluxo E2E funciona no browser. Orcamento criado aparece na lista.

---

## Entregavel
- [x] Clientes CRUD funcionando com permissoes
- [x] Orcamentos sendo criados com calculos corretos
- [x] Deslocamento calculado (Google Maps + fallback)
- [x] Frontend conectado e funcional para orcamentos (integrado ao docker-compose)
