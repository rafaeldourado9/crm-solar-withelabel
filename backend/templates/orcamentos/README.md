# Templates de Orçamentos

Coloque aqui os modelos de orçamentos em formato DOCX/PDF com as seguintes chaves:

## Chaves Disponíveis

### Dados do Cliente
- `{{cliente_nome}}`
- `{{cliente_cpf_cnpj}}`
- `{{cliente_endereco}}`
- `{{cliente_cidade}}`
- `{{cliente_estado}}`
- `{{cliente_telefone}}`
- `{{cliente_email}}`

### Dados do Sistema
- `{{potencia_total}}`
- `{{quantidade_paineis}}`
- `{{modelo_painel}}`
- `{{potencia_painel}}`
- `{{quantidade_inversores}}`
- `{{modelo_inversor}}`
- `{{potencia_inversor}}`
- `{{geracao_estimada}}`
- `{{consumo_mensal}}`

### Dados Financeiros
- `{{valor_equipamentos}}`
- `{{valor_montagem}}`
- `{{valor_projeto}}`
- `{{valor_deslocamento}}`
- `{{valor_total}}`
- `{{valor_final}}`
- `{{forma_pagamento}}`
- `{{numero_parcelas}}`
- `{{valor_parcela}}`

### Dados do Orçamento
- `{{numero_orcamento}}`
- `{{data_orcamento}}`
- `{{validade_dias}}`
- `{{vendedor_nome}}`

## Exemplo de Uso no DOCX

```
ORÇAMENTO Nº {{numero_orcamento}}

Cliente: {{cliente_nome}}
CPF/CNPJ: {{cliente_cpf_cnpj}}
Endereço: {{cliente_endereco}}, {{cliente_cidade}}/{{cliente_estado}}

Sistema Fotovoltaico:
- Potência: {{potencia_total}} kWp
- Painéis: {{quantidade_paineis}}x {{modelo_painel}} ({{potencia_painel}}W)
- Inversor: {{quantidade_inversores}}x {{modelo_inversor}} ({{potencia_inversor}}kW)
- Geração Estimada: {{geracao_estimada}} kWh/mês

VALOR TOTAL: R$ {{valor_final}}
```
