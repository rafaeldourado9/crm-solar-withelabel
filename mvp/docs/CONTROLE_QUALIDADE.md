# Controle de Qualidade - SunOps SaaS MVP

## Metricas Obrigatorias

| Metrica | Target | Ferramenta | Enforcement |
|---------|--------|------------|-------------|
| Cobertura de testes | >= 80% | pytest-cov | CI bloqueia merge |
| Complexidade Ciclomatica | <= 5 | radon | CI bloqueia merge |
| Type checking | strict | mypy | CI bloqueia merge |
| Linting | zero warnings | ruff | Pre-commit hook |
| Formatacao | consistente | ruff format | Pre-commit hook |

## Piramide de Testes

```
         /  E2E  \         10% - API endpoints (httpx AsyncClient)
        /----------\
       / Integration \     30% - Use cases com banco real
      /----------------\
     /    Unit Tests     \  60% - Domain services (logica pura)
    /______________________\
```

### Testes Unitarios (Domain)
- SolarCalculatorService: cada formula testada isoladamente
- DeslocamentoCalculator: cidades com/sem cobranca
- ComissaoCalculator: calculo de comissao
- TemplateEngine: substituicao de variaveis
- Value Objects: validacao CPF, CNPJ, Money
- Entidades: transicoes de status

```python
# Exemplo - teste do calculo de markup
def test_aplicar_margens_18_5_6_retorna_valor_correto():
    service = SolarCalculatorService()
    subtotal = Decimal("10000")
    margem = MargemConfig(lucro=18, comissao=5, imposto=6)

    resultado = service.aplicar_margens(subtotal, margem)

    # 10000 / (1 - 0.29) = 14084.51 -> arredonda para 14100
    assert resultado == Decimal("14100")
```

### Testes de Integracao (Application)
- Use cases com banco PostgreSQL real
- Isolamento por tenant verificado
- Transacoes e rollbacks

```python
# Exemplo - isolamento de tenant
async def test_listar_clientes_nao_retorna_de_outro_tenant(db, tenant_a, tenant_b):
    await criar_cliente(db, tenant_id=tenant_a.id, nome="Cliente A")
    await criar_cliente(db, tenant_id=tenant_b.id, nome="Cliente B")

    use_case = ListarClientesUseCase(repo)
    resultado = await use_case.execute(tenant_id=tenant_a.id)

    assert len(resultado) == 1
    assert resultado[0].nome == "Cliente A"
```

### Testes E2E (API)
- Endpoints com autenticacao JWT
- Fluxos completos (criar orcamento -> proposta -> contrato)
- Download de documentos

## Complexidade Ciclomatica

### Regras
- CC 1-5: OK (simples, testavel)
- CC 6-10: Refatorar (decompor em funcoes menores)
- CC > 10: Proibido (nao passa no CI)

### Como manter CC baixa
1. **Early returns** ao inves de if/else aninhado
2. **Strategy pattern** ao inves de switch/case
3. **Funcoes pequenas** (max 20 linhas)
4. **Separar validacao de logica**
5. **Dict lookup** ao inves de cadeia de if/elif

```python
# RUIM - CC = 7
def calcular_material_eletrico(potencia_kwp):
    if potencia_kwp <= 3:
        return 250
    elif potencia_kwp <= 5:
        return 350
    elif potencia_kwp <= 6:
        return 400
    elif potencia_kwp <= 8:
        return 500
    elif potencia_kwp <= 10:
        return 900
    else:
        return 1200

# BOM - CC = 2
def calcular_material_eletrico(potencia_kwp: Decimal, faixas: list[FaixaPotencia]) -> Decimal:
    for faixa in faixas:
        if faixa.potencia_min <= potencia_kwp < faixa.potencia_max:
            return faixa.valor
    return faixas[-1].valor  # fallback para ultima faixa
```

## Pre-commit Hooks

```yaml
# .pre-commit-config.yaml
repos:
  - repo: local
    hooks:
      - id: ruff-check
        name: ruff lint
        entry: ruff check --fix
        language: python
        types: [python]

      - id: ruff-format
        name: ruff format
        entry: ruff format
        language: python
        types: [python]

      - id: mypy
        name: mypy type check
        entry: mypy src/
        language: python
        types: [python]

      - id: radon
        name: radon cc check
        entry: radon cc src/ -a -nc
        language: python
        types: [python]
```

## CI Pipeline

```
Push/PR -> Lint (ruff) -> Types (mypy) -> CC (radon) -> Tests (pytest) -> Coverage check
```

Qualquer falha bloqueia o merge.
