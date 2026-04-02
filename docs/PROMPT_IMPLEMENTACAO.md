# PROMPT DE IMPLEMENTACAO - SunOps SaaS MVP

Cole este prompt inteiro no agente de IA. Ele contem tudo que e necessario para implementar o projeto.

---

## PROMPT INICIO

Voce e um engenheiro de software senior especializado em Python, FastAPI e arquitetura hexagonal. Sua tarefa e implementar o backend do SunOps SaaS MVP — uma plataforma WhiteLabel para empresas de energia solar.

## REGRAS INEGOCIAVEIS

1. **TDD OBRIGATORIO**: Escreva o teste ANTES do codigo. Nenhum modulo e considerado pronto se `pytest` nao passar com 80%+ de cobertura.
2. **TESTES TEM QUE PASSAR**: Ao final de CADA modulo, rode `pytest` e mostre a saida. Se falhar, corrija ate passar. NAO avance para o proximo modulo com testes falhando.
3. **CC <= 5**: Nenhuma funcao pode ter complexidade ciclomatica maior que 5. Use early returns, dict lookups e decomposicao.
4. **Domain PURO**: A camada domain/ NAO pode importar SQLAlchemy, FastAPI, Redis ou qualquer lib externa. Apenas stdlib + pydantic.
5. **Isolamento total por tenant**: Toda query filtra por tenant_id. Teste de isolamento obrigatorio.
6. **Decimal para dinheiro**: NUNCA use float para valores monetarios. Sempre `Decimal`.
7. **Async-first**: Todos os endpoints e repositorios sao `async`.

## STACK

- Python 3.12+
- FastAPI 0.109+
- SQLAlchemy 2.0 (async, com asyncpg)
- Alembic (migracoes)
- PostgreSQL 15
- Redis 7 (cache + JWT blacklist)
- pytest + pytest-asyncio + httpx (testes)
- python-docx (geracao DOCX)
- Pydantic v2 (validacao + DTOs)
- passlib[bcrypt] (senhas)
- python-jose[cryptography] (JWT)
- ruff (lint + format)

## ARQUITETURA HEXAGONAL

Cada modulo (bounded context) segue EXATAMENTE esta estrutura:

```
modulo/
  __init__.py
  domain/
    __init__.py
    entities.py        # Entidades de dominio (Pydantic BaseModel ou dataclass)
    value_objects.py   # Value Objects imutaveis (opcional)
    repositories.py    # Port - Protocol abstrato
    services.py        # Logica de negocio PURA (zero imports externos)
    exceptions.py      # Excecoes de dominio
  application/
    __init__.py
    use_cases.py       # Orquestracao
    dtos.py            # Schemas Pydantic (request/response)
  infrastructure/
    __init__.py
    models.py          # SQLAlchemy models
    repositories.py    # Implementacao concreta do repo
    api.py             # FastAPI router
    dependencies.py    # Depends() factories
  tests/
    __init__.py
    test_domain.py     # Testes unitarios (SEM banco)
    test_use_cases.py  # Testes de integracao (COM banco)
    test_api.py        # Testes E2E (httpx AsyncClient)
    conftest.py        # Fixtures do modulo
```

**REGRA DE DEPENDENCIA:**
- domain/ NAO importa application/ nem infrastructure/
- application/ importa domain/, NAO importa infrastructure/
- infrastructure/ importa tudo (implementa os ports)
- FastAPI Depends() injeta os adapters nos use cases

## ESTRUTURA COMPLETA DO PROJETO

```
mvp/backend/
  pyproject.toml
  alembic.ini
  alembic/env.py
  alembic/versions/
  src/
    main.py              # App factory, inclui todos os routers
    config.py            # Settings via pydantic-settings
    database.py          # async engine + session maker
    shared/              # Kernel compartilhado
      base_entity.py     # id(UUID), created_at, updated_at
      base_model.py      # SQLAlchemy Base + TenantMixin
      base_repository.py # Repo abstrato com filtro tenant_id
      exceptions.py      # DomainError, NotFoundError, ForbiddenError
      value_objects.py   # Money, CPF, CNPJ
      utils.py           # numero_por_extenso(), format_brl()
    tenant/              # Multi-tenancy
    auth/                # JWT auth
    premissas/           # Regras de negocio configuraveis
    equipamentos/        # Paineis e inversores
    clientes/            # Gestao de clientes
    deslocamento/        # Calculo distancia/custo viagem
    orcamentos/          # CORE: calculo solar e pricing
    propostas/           # Propostas comerciais
    contratos/           # Contratos + geracao DOCX
    documentos/          # Engine de templates DOCX/PDF
    vendedores/          # Equipe comercial + comissoes
    dashboard/           # Analytics/KPIs
  tests/
    conftest.py          # Fixtures globais (db session, test client, tenant)
    test_health.py
```

## MODULO TENANT (modelo)

```python
# Campos obrigatorios da entidade Tenant:
Tenant:
  id: UUID
  nome_fantasia: str
  razao_social: str
  cnpj: str
  endereco: str
  cidade: str
  estado: str (2 chars)
  cep: str
  representante_nome: str
  representante_cpf: str
  representante_rg: str
  banco_nome: str
  banco_agencia: str
  banco_conta: str
  banco_titular: str
  logo_url: str | None
  cor_primaria: str (hex, default "#1E40AF")
  cor_secundaria: str (hex, default "#F59E0B")
  dominio_customizado: str | None
  plano: "free" | "pro" | "enterprise"
  ativo: bool (default True)
  created_at: datetime
  updated_at: datetime
```

## MODULO AUTH

- JWT com access token (15min) + refresh token (7 dias)
- Access token payload: { user_id, tenant_id, role, exp }
- Roles: "admin", "vendedor", "indicacao"
- POST /api/v1/auth/login -> { access_token, refresh_token }
- POST /api/v1/auth/refresh -> { access_token }
- POST /api/v1/auth/logout -> invalida refresh no Redis
- Dependency `get_current_user` extrai user do JWT
- Dependency `get_current_tenant` extrai tenant do JWT

## MODULO PREMISSAS

Singleton por tenant. Campos:

```
margem_lucro_percentual: Decimal (default 18)
comissao_percentual: Decimal (default 5)
imposto_percentual: Decimal (default 6)
margem_desconto_avista_percentual: Decimal (default 2)
montagem_por_painel: Decimal (default 70)
valor_projeto: Decimal (default 400)
hsp_padrao: Decimal (default 5.5)
perda_padrao: Decimal (default 0.20)
overload_inversor: Decimal (default 0.70)
tarifa_energia_atual: Decimal (default 0.95)
inflacao_energetica_anual: Decimal (default 0.08)
perda_eficiencia_anual: Decimal (default 0.005)
faixas_material_eletrico: JSON [{"potencia_min": 0, "potencia_max": 3, "valor": 250}, ...]
taxas_maquininha: JSON {"2": 2.5, "3": 3.5, "6": 5.0, "12": 8.0}
consumo_veiculo: Decimal (default 10)
preco_combustivel: Decimal (default 6.75)
margem_deslocamento: Decimal (default 0.20)
cidades_sem_cobranca: JSON ["Itapora", "Dourados"]
```

## MODULO ORCAMENTOS - REGRAS DE CALCULO (CRITICO)

Este e o coracao do sistema. Implemente EXATAMENTE estas formulas:

### 1. Dimensionamento Tecnico
```
potencia_necessaria_kw = consumo_mensal / (hsp * 30 * (1 - perda))
quantidade_paineis = CEIL(potencia_necessaria_kw * 1000 / painel.potencia_w)
potencia_sistema_kwp = (quantidade_paineis * painel.potencia_w) / 1000
geracao_mensal_kwh = potencia_sistema_kwp * hsp * 30 * (1 - perda)
```

### 2. Validacao Inversor
```
potencia_maxima_inversor = inversor.potencia_nominal_w * (1 + overload)
potencia_paineis_total = quantidade_paineis * painel.potencia_w
REGRA: potencia_paineis_total <= potencia_maxima_inversor
```

### 3. Calculo Subtotal
```
SUBTOTAL = valor_kit
         + (montagem_por_painel * quantidade_paineis)
         + valor_projeto
         + valor_estrutura
         + valor_material_eletrico  (lookup pela potencia do INVERSOR em kWp nas faixas)
         + SUM(itens_adicionais)
         + custo_deslocamento
```

### 4. Calculo Deslocamento
```
SE cidade IN cidades_sem_cobranca: custo = 0
SENAO:
  distancia_total = distancia_km * 2
  litros = distancia_total / consumo_veiculo
  custo_combustivel = litros * preco_combustivel
  custo = custo_combustivel * (1 + margem_deslocamento)
```

### 5. Markup (Valor Final)
```
total_pct = (comissao + imposto + margem_lucro) / 100
valor_base = SUBTOTAL / (1 - total_pct)
valor_base_arredondado = CEIL(valor_base / 100) * 100

margem_desconto = valor_base_arredondado * (margem_desconto_avista / 100)
valor_com_margem = valor_base_arredondado + margem_desconto
VALOR_FINAL = CEIL(valor_com_margem / 100) * 100
```

### 6. Juros (Parcelas)
```
SE forma_pagamento == "avista": valor_cobrado = VALOR_FINAL
SENAO:
  taxa = taxas_maquininha[forma_pagamento]
  valor_cobrado = VALOR_FINAL * (1 + taxa / 100)
  valor_parcela = valor_cobrado / int(forma_pagamento)
```

### 7. Economia Projetada (25 anos)
```
Para ano in 1..25:
  tarifa = tarifa_atual * (1 + inflacao) ^ ano
  geracao = geracao_mensal * 12 * (1 - perda_eficiencia * ano / 100)
  economia_ano = geracao * tarifa
  acumulada += economia_ano
```

## TESTES OBRIGATORIOS DO SOLAR CALCULATOR

Implemente TODOS estes testes. Todos devem passar:

```python
# test_domain.py - SolarCalculatorService

# --- Dimensionamento ---
def test_dimensionar_consumo_500kwh_painel_550w():
    """500 kWh/mes, painel 550W, HSP 5.5, perda 20%
    potencia_necessaria = 500 / (5.5 * 30 * 0.80) = 3.787 kW
    qtd_paineis = CEIL(3787 / 550) = 7
    potencia_kwp = 7 * 550 / 1000 = 3.850
    geracao = 3.85 * 5.5 * 30 * 0.80 = 508.20 kWh"""
    # resultado.quantidade_paineis == 7
    # resultado.potencia_kwp == Decimal("3.850")

def test_dimensionar_consumo_1000kwh_painel_550w():
    """1000 kWh/mes -> 14 paineis, 7.700 kWp"""

def test_dimensionar_consumo_baixo_retorna_minimo_1_painel():
    """Consumo muito baixo ainda retorna ao menos 1 painel"""

# --- Validacao Inversor ---
def test_validar_inversor_dentro_do_limite():
    """7 paineis * 550W = 3850W <= 5000 * 1.70 = 8500W -> OK"""

def test_validar_inversor_excede_limite_levanta_erro():
    """20 paineis * 550W = 11000W > 5000 * 1.70 = 8500W -> ERRO"""

# --- Material Eletrico ---
def test_material_eletrico_inversor_4kwp_retorna_350():
    """4 kWp esta na faixa 3-5 -> R$ 350"""

def test_material_eletrico_inversor_7kwp_retorna_500():
    """7 kWp esta na faixa 6-8 -> R$ 500"""

# --- Subtotal ---
def test_calcular_subtotal_completo():
    """valor_kit=15000 + montagem(7*70=490) + projeto(400) + estrutura(800)
       + material_eletrico(350) + itens_adicionais(200) + deslocamento(150)
       = 17390"""

# --- Markup ---
def test_aplicar_margens_padrao():
    """Subtotal 17390, margens 18+5+6=29%
    valor_base = 17390 / (1-0.29) = 24492.96 -> arredonda 24500
    margem_desconto = 24500 * 0.02 = 490
    valor_com_margem = 24990 -> arredonda 25000
    VALOR_FINAL = 25000"""

def test_markup_arredonda_para_centena_superior():
    """Qualquer valor quebrado arredonda para cima na centena"""

# --- Juros ---
def test_avista_sem_juros():
    """forma_pagamento='avista' -> valor_final inalterado"""

def test_parcelado_12x_aplica_8_porcento():
    """25000 * 1.08 = 27000, parcela = 27000/12 = 2250"""

def test_parcelado_6x_aplica_5_porcento():
    """25000 * 1.05 = 26250, parcela = 26250/6 = 4375"""

# --- Deslocamento ---
def test_cidade_isenta_custo_zero():
    """Itapora ou Dourados -> custo = 0"""

def test_deslocamento_100km():
    """100km * 2 = 200km / 10 km/L = 20L * 6.75 = 135 * 1.20 = 162"""

# --- Economia 25 anos ---
def test_economia_ano_1():
    """geracao_mensal * 12 * (1 - 0.005) * tarifa * (1.08)
    508.20 * 12 * 0.995 * 0.95 * 1.08 = ~6230"""

def test_economia_acumulada_25_anos_positiva():
    """Deve retornar valor > 0 e crescente"""

# --- Isolamento Tenant ---
async def test_orcamento_tenant_a_nao_visivel_por_tenant_b():
    """Criar orcamento no tenant A, buscar pelo tenant B -> nao encontra"""
```

## MODULO DOCUMENTOS (DOCX)

### Engine de substituicao de variaveis

O problema do projeto antigo era que o python-docx fragmenta texto em multiplos "runs" dentro de um paragrafo. Exemplo: `{{CLIENTE_NOME}}` pode virar 3 runs: `{{CLIENTE_`, `NOME`, `}}`.

**SOLUCAO**: Concatenar todo o texto do paragrafo, fazer a substituicao, e reescrever:

```python
def substituir_variaveis_paragrafo(paragraph, variables: dict[str, str]):
    """Concatena todos os runs, substitui, reescreve no primeiro run, limpa os demais"""
    full_text = "".join(run.text for run in paragraph.runs)
    if not any(f"{{{{{k}}}}}" in full_text for k in variables):
        return
    for key, value in variables.items():
        full_text = full_text.replace(f"{{{{{key}}}}}", value)
    for i, run in enumerate(paragraph.runs):
        if i == 0:
            run.text = full_text
        else:
            run.text = ""
```

Variaveis de contrato (28 total):
- Cliente: cliente_nome, cliente_cpf_cnpj, cliente_endereco, cliente_bairro, cliente_cidade, cliente_estado, cliente_cep
- Empresa (DO TENANT, nao hardcoded): empresa_razao_social, empresa_cnpj, empresa_endereco, empresa_cidade, empresa_cep, empresa_representante_nome, empresa_representante_cpf, empresa_representante_rg
- Banco (DO TENANT): banco_nome, banco_agencia, banco_conta, banco_titular
- Equipamento: potencia_total, quantidade_paineis, valor_total, valor_total_extenso, numero_parcelas, valor_parcela, valor_parcela_extenso
- Termos: prazo_execucao_dias, garantia_instalacao_meses, foro_comarca

### Teste obrigatorio:
```python
def test_substituir_variaveis_em_runs_fragmentados():
    """Cria um paragrafo com {{CLIENTE_NOME}} fragmentado em 3 runs
    e verifica que a substituicao funciona"""

def test_todas_28_variaveis_contrato_substituidas():
    """Cria template com todas as 28 variaveis e verifica que nenhuma fica como {{...}}"""

def test_substituicao_em_tabelas():
    """Variaveis dentro de celulas de tabela tambem sao substituidas"""
```

## FLUXO COMERCIAL

```
Cliente(status=orcamento)
  -> Orcamento(criado com calculo automatico)
    -> POST /orcamentos/{id}/converter-proposta
      -> Proposta(status=pendente) + Cliente(status=proposta)
        -> POST /propostas/{id}/aceitar
          -> Proposta(status=aceita)
            -> Contrato(criado automatico) + Cliente(status=contrato)
              -> GET /contratos/{id}/gerar-docx
                -> Download DOCX com variaveis do TENANT
```

## API ENDPOINTS (todos sob /api/v1)

### Auth
- POST /auth/login -> {access_token, refresh_token}
- POST /auth/refresh -> {access_token}
- POST /auth/logout

### Tenants
- POST /tenants (signup)
- GET /tenants/me
- PUT /tenants/me
- PUT /tenants/me/branding

### Clientes
- GET/POST /clientes
- GET/PUT/DELETE /clientes/{id}

### Equipamentos
- GET/POST /paineis
- GET/POST /inversores
- POST /equipamentos/validar-dimensionamento

### Premissas
- GET /premissas/ativa
- PUT /premissas/{id}

### Orcamentos
- GET/POST /orcamentos
- GET/PUT/DELETE /orcamentos/{id}
- POST /orcamentos/{id}/converter-proposta
- POST /orcamentos/{id}/gerar-pdf
- POST /orcamentos/calcular-material-eletrico

### Deslocamento
- POST /deslocamento/calcular

### Propostas
- GET /propostas
- GET /propostas/{id}
- POST /propostas/{id}/aceitar
- POST /propostas/{id}/recusar

### Contratos
- GET /contratos
- GET /contratos/{id}
- PUT /contratos/{id}
- GET /contratos/{id}/gerar-docx
- GET /contratos/{id}/gerar-pdf

### Templates
- GET/POST /templates
- PUT /templates/{id}/ativar
- DELETE /templates/{id}

### Vendedores
- GET/POST /vendedores
- PUT /vendedores/{id}
- POST /vendedores/{id}/bloquear
- POST /vendedores/{id}/resetar-senha
- GET /vendedores/{id}/resumo
- GET /vendedores/{id}/historico-vendas

### Dashboard
- GET /dashboard/resumo

### Health
- GET /health

## ORDEM DE IMPLEMENTACAO

Implemente nesta ordem exata. Ao final de CADA passo, rode `pytest -v` e mostre a saida:

### Passo 1: Setup
- pyproject.toml com todas as deps
- config.py (pydantic-settings)
- database.py (async engine)
- shared/ (base classes, exceptions, utils)
- main.py (app factory com health check)
- tests/conftest.py (fixtures: db, client, tenant)
- **RODE: `pytest tests/test_health.py -v` -> DEVE PASSAR**

### Passo 2: Tenant + Auth
- tenant/ (domain + infra + api)
- auth/ (domain + infra + api + middleware)
- Migracao Alembic
- **RODE: `pytest tenant/ auth/ -v` -> DEVE PASSAR**

### Passo 3: Premissas + Equipamentos
- premissas/ (domain + infra + api)
- equipamentos/ (domain + infra + api)
- **RODE: `pytest premissas/ equipamentos/ -v` -> DEVE PASSAR**

### Passo 4: Clientes + Deslocamento
- clientes/ (domain + infra + api)
- deslocamento/ (domain + infra + api)
- **RODE: `pytest clientes/ deslocamento/ -v` -> DEVE PASSAR**

### Passo 5: Orcamentos (CORE)
- orcamentos/domain/ PRIMEIRO (SolarCalculatorService + testes)
- orcamentos/application/ + infrastructure/
- **RODE: `pytest orcamentos/ -v` -> TODOS OS TESTES DE CALCULO DEVEM PASSAR**

### Passo 6: Documentos + Propostas + Contratos
- documentos/ (engine de templates DOCX)
- propostas/ (domain + infra + api)
- contratos/ (domain + infra + api + geracao DOCX)
- **RODE: `pytest documentos/ propostas/ contratos/ -v` -> DEVE PASSAR**

### Passo 7: Vendedores + Dashboard
- vendedores/ (domain + infra + api)
- dashboard/ (application + api)
- **RODE: `pytest vendedores/ dashboard/ -v` -> DEVE PASSAR**

### Passo 8: Teste final
```bash
pytest --cov=src --cov-report=term-missing -v
```
**COBERTURA MINIMA: 80%. Se nao atingir, adicione testes ate atingir.**

## DOCKER

Crie `docker-compose.yml`:
```yaml
services:
  db:
    image: postgres:15-alpine
    environment:
      POSTGRES_DB: sunops
      POSTGRES_USER: sunops
      POSTGRES_PASSWORD: sunops123
    ports: ["5432:5432"]

  redis:
    image: redis:7-alpine
    ports: ["6379:6379"]

  api:
    build: ./backend
    ports: ["8000:8000"]
    depends_on: [db, redis]
    environment:
      DATABASE_URL: postgresql+asyncpg://sunops:sunops123@db:5432/sunops
      REDIS_URL: redis://redis:6379/0
      SECRET_KEY: dev-secret-key-change-in-production
      DEBUG: "true"
```

## CHECKLIST FINAL

Antes de dizer que terminou, verifique:

- [ ] `pytest --cov=src -v` passa com 80%+ cobertura
- [ ] Nenhuma funcao com CC > 5
- [ ] Domain layer nao importa SQLAlchemy/FastAPI
- [ ] Todos os valores monetarios usam Decimal
- [ ] Todos os endpoints sao async
- [ ] Tenant isolamento testado (dados de tenant A nao vazam para B)
- [ ] Calculo solar bate com os exemplos dos testes
- [ ] Variaveis DOCX substituidas corretamente (inclusive runs fragmentados)
- [ ] Dados da empresa no contrato vem do Tenant (nao hardcoded)
- [ ] `docker compose up` sobe sem erros
- [ ] GET /health retorna 200

SE ALGUM TESTE FALHAR, CORRIJA ANTES DE PROSSEGUIR. NAO AVANCE COM TESTES QUEBRADOS.

## PROMPT FIM
