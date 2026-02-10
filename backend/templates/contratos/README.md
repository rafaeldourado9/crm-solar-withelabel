# Templates de Contratos

Coloque aqui os modelos de contratos em formato DOCX com as seguintes chaves:

## Chaves Disponíveis

### Dados do Cliente (CONTRATANTE)
- `{{cliente_nome}}`
- `{{cliente_cpf_cnpj}}`
- `{{cliente_endereco}}`
- `{{cliente_bairro}}`
- `{{cliente_cidade}}`
- `{{cliente_estado}}`
- `{{cliente_cep}}`
- `{{cliente_telefone}}`
- `{{cliente_email}}`

### Dados da Empresa (CONTRATADA)
- `{{empresa_razao_social}}`
- `{{empresa_cnpj}}`
- `{{empresa_endereco}}`
- `{{empresa_cidade}}`
- `{{empresa_estado}}`
- `{{empresa_cep}}`
- `{{empresa_representante_nome}}`
- `{{empresa_representante_cpf}}`
- `{{empresa_representante_rg}}`

### Dados do Sistema
- `{{potencia_total}}`
- `{{quantidade_paineis}}`
- `{{modelo_painel}}`
- `{{potencia_painel}}`
- `{{quantidade_inversores}}`
- `{{modelo_inversor}}`
- `{{potencia_inversor}}`
- `{{geracao_estimada}}`

### Dados Financeiros
- `{{valor_total}}`
- `{{valor_total_extenso}}`
- `{{forma_pagamento}}`
- `{{descricao_pagamento}}`
- `{{numero_parcelas}}`
- `{{valor_parcela}}`
- `{{valor_parcela_extenso}}`

### Dados Bancários
- `{{banco_nome}}`
- `{{banco_agencia}}`
- `{{banco_conta}}`
- `{{banco_titular}}`

### Datas e Prazos
- `{{data_assinatura}}`
- `{{prazo_execucao_dias}}`
- `{{garantia_instalacao_meses}}`

### Outros
- `{{numero_contrato}}`
- `{{foro_comarca}}`

## Exemplo de Uso no DOCX

```
CONTRATO DE PRESTAÇÃO DE SERVIÇOS Nº {{numero_contrato}}

CONTRATANTE: {{cliente_nome}}, inscrito no CPF/CNPJ sob nº {{cliente_cpf_cnpj}}, 
residente e domiciliado à {{cliente_endereco}}, {{cliente_bairro}}, 
{{cliente_cidade}}/{{cliente_estado}}, CEP {{cliente_cep}}.

CONTRATADA: {{empresa_razao_social}}, inscrita no CNPJ sob nº {{empresa_cnpj}}...

VALOR TOTAL: R$ {{valor_total}} ({{valor_total_extenso}})
```
