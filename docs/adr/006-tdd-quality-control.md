# ADR-006: TDD e Controle de Qualidade

## Status
Aceita

## Contexto
Projeto atual nao tem testes. Bugs no calculo solar, templates e contratos
so sao descobertos em producao.

## Decisao
TDD obrigatorio com metricas de qualidade enforced.

## Regras

### Testes
- **Unit tests**: Domain services (calculos, validacoes) - pytest
- **Integration tests**: Use cases com banco real - pytest-asyncio
- **E2E tests**: API endpoints - httpx AsyncClient
- **Cobertura minima**: 80%

### Complexidade Ciclomatica
- Maximo CC = 5 por funcao
- Enforced via `radon` no CI
- Funcoes com CC > 5 devem ser decompostas

### Linting
- `ruff` para linting + formatting
- `mypy` para type checking (strict mode)
- Pre-commit hooks para garantir

### Naming
- Testes: `test_<acao>_<condicao>_<resultado_esperado>`
- Exemplo: `test_calcular_valor_final_com_parcelas_aplica_juros`

## Estrutura de Teste

```python
# test_domain.py - SolarCalculator
def test_dimensionar_consumo_500kwh_retorna_8_paineis():
    calc = SolarCalculatorService()
    resultado = calc.dimensionar(
        consumo_mensal=Decimal("500"),
        painel=PainelConfig(potencia_w=550),
        hsp=Decimal("5.5"),
        perda=Decimal("0.20"),
    )
    assert resultado.quantidade_paineis == 8
    assert resultado.potencia_kwp == Decimal("4.400")
```
