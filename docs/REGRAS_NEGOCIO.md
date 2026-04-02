# Regras de Negocio - SunOps SaaS

## 1. Premissas (Configuracoes Globais por Tenant)

Cada tenant possui uma instancia ativa de Premissas com:

### Margens e Custos
| Campo | Default | Descricao |
|-------|---------|-----------|
| margem_lucro_percentual | 18% | Margem de lucro sobre custo |
| comissao_percentual | 5% | Comissao do vendedor |
| imposto_percentual | 6% | Carga tributaria |
| margem_desconto_avista | 2% | Colchao para desconto a vista |
| montagem_por_painel | R$ 70 | Custo mao-de-obra por painel |
| valor_projeto | R$ 400 | Custo fixo de projeto eletrico |

### Parametros Tecnicos
| Campo | Default | Descricao |
|-------|---------|-----------|
| hsp_padrao | 5.5 h | Horas de Sol Pico (Dourados/MS) |
| perda_padrao | 20% | Perdas do sistema (sujeira, temperatura, cabeamento) |
| overload_inversor | 0.70 | Fator adicional de overload (70% acima da nominal) |

### Energia
| Campo | Default | Descricao |
|-------|---------|-----------|
| tarifa_energia_atual | R$ 0.95/kWh | Tarifa da concessionaria |
| inflacao_energetica_anual | 8% | Reajuste anual projetado |
| perda_eficiencia_anual | 0.5% | Degradacao dos paineis por ano |

### Taxas Maquininha (JSON)
```json
{
  "2": 2.5,
  "3": 3.5,
  "6": 5.0,
  "12": 8.0
}
```

### Material Eletrico por Faixa de Potencia (JSON)
```json
[
  {"potencia_min": 0, "potencia_max": 3, "valor": 250},
  {"potencia_min": 3, "potencia_max": 5, "valor": 350},
  {"potencia_min": 5, "potencia_max": 6, "valor": 400},
  {"potencia_min": 6, "potencia_max": 8, "valor": 500},
  {"potencia_min": 8, "potencia_max": 10, "valor": 900}
]
```
**IMPORTANTE**: Potencia usada e a do INVERSOR, nao dos paineis.

### Deslocamento
| Campo | Default | Descricao |
|-------|---------|-----------|
| consumo_veiculo | 10 km/L | Consumo medio do veiculo |
| preco_combustivel | R$ 6.75/L | Preco do combustivel |
| margem_deslocamento | 20% | Markup sobre custo real |
| cidades_sem_cobranca | ["Itapora", "Dourados"] | Cidades isentas de deslocamento |

---

## 2. Fluxo de Orcamento (Calculo Solar)

### 2.1 Dimensionamento Tecnico

```
Entrada: consumo_mensal_kwh, painel (potencia_w), hsp, perda

potencia_necessaria_kw = consumo_mensal / (hsp * 30 * (1 - perda))
quantidade_paineis = TETO(potencia_necessaria_kw * 1000 / painel.potencia_w)
potencia_sistema_kwp = (quantidade_paineis * painel.potencia_w) / 1000
geracao_mensal_kwh = potencia_sistema_kwp * hsp * 30 * (1 - perda)
```

### 2.2 Validacao Inversor

```
potencia_maxima_inversor = inversor.potencia_nominal * (1 + overload)
potencia_paineis_total = quantidade_paineis * painel.potencia_w

REGRA: potencia_paineis_total <= potencia_maxima_inversor
  Se NAO: Erro "Potencia dos paineis excede capacidade do inversor"
```

### 2.3 Calculo de Custos (Subtotal)

```
SUBTOTAL = valor_kit (paineis + inversor)
         + (montagem_por_painel * quantidade_paineis)
         + valor_projeto
         + valor_estrutura (por tipo: ceramico, zinco, solo, laje...)
         + valor_material_eletrico (lookup pela potencia do INVERSOR)
         + SUM(itens_adicionais[].valor)
         + custo_deslocamento
```

### 2.4 Calculo de Deslocamento

```
SE cidade_cliente IN cidades_sem_cobranca:
    custo = 0
SENAO:
    distancia_km = GoogleMaps(origem, destino) OU tabela_fallback
    distancia_total = distancia_km * 2  (ida e volta)
    litros = distancia_total / consumo_veiculo
    custo_combustivel = litros * preco_combustivel
    custo_cliente = custo_combustivel * (1 + margem_deslocamento)
```

### 2.5 Calculo Valor Final (Markup)

```
total_percentual = (comissao + imposto + margem_lucro) / 100
valor_base = SUBTOTAL / (1 - total_percentual)
valor_base_arredondado = TETO(valor_base / 100) * 100

margem_desconto = valor_base_arredondado * (margem_desconto_avista / 100)
valor_com_margem = valor_base_arredondado + margem_desconto
VALOR_FINAL = TETO(valor_com_margem / 100) * 100
```

### 2.6 Aplicacao de Juros (Parcelas)

```
SE forma_pagamento == "avista":
    valor_cobrado = VALOR_FINAL
SENAO:
    parcelas = int(forma_pagamento)  // "12" -> 12
    taxa = taxas_maquininha[forma_pagamento]  // 12 -> 8%
    valor_cobrado = VALOR_FINAL * (1 + taxa / 100)
    valor_parcela = valor_cobrado / parcelas
```

### 2.7 Economia Projetada (25 anos)

```
Para cada ano (1..25):
    tarifa_ano = tarifa_atual * (1 + inflacao_energetica) ^ ano
    geracao_ano = geracao_mensal * 12 * (1 - perda_eficiencia * ano / 100)
    economia_ano = geracao_ano * tarifa_ano
    economia_acumulada += economia_ano
```

---

## 3. Fluxo Comercial

```
Cliente -> Orcamento -> Proposta -> Contrato -> OS (Ordem de Servico)

Status Cliente:  orcamento -> proposta -> contrato
Status Proposta: pendente -> aceita | recusada
Status Contrato: rascunho -> assinado -> em_execucao -> concluido
```

### Conversao Orcamento -> Proposta
- Copia dados do cliente e margens do orcamento
- Gera numero sequencial da proposta
- Seta status do cliente para "proposta"

### Conversao Proposta -> Contrato
- Vincula proposta ao contrato (OneToOne)
- Copia dados de equipamentos, valores, parcelas
- **Dados da empresa vem do TENANT** (nao hardcoded)
- Seta status do cliente para "contrato"

---

## 4. Geracao de Documentos

### Variaveis Template Orcamento (40+)

**Cliente:**
`{{NUMERO_ORCAMENTO}}`, `{{CLIENTE_NOME}}`, `{{CLIENTE_ENDERECO}}`, `{{CLIENTE_CIDADE}}`, `{{CLIENTE_ESTADO}}`, `{{CLIENTE_CPF_CNPJ}}`, `{{CLIENTE_EMAIL}}`, `{{CLIENTE_TELEFONE}}`

**Tecnico:**
`{{POTENCIA_KWP}}`, `{{QUANTIDADE_PAINEIS}}`, `{{MODELO_PAINEL}}`, `{{POTENCIA_PAINEL_W}}`, `{{MODELO_INVERSOR}}`, `{{POTENCIA_INVERSOR_W}}`, `{{GERACAO_MENSAL_KWH}}`, `{{AREA_NECESSARIA_M2}}`

**Financeiro:**
`{{VALOR_KIT}}`, `{{VALOR_ESTRUTURA}}`, `{{VALOR_MATERIAL_ELETRICO}}`, `{{VALOR_MONTAGEM}}`, `{{VALOR_PROJETO}}`, `{{CUSTO_DESLOCAMENTO}}`, `{{SUBTOTAL}}`, `{{VALOR_FINAL}}`, `{{FORMA_PAGAMENTO}}`, `{{NUMERO_PARCELAS}}`, `{{VALOR_PARCELA}}`, `{{TAXA_JUROS}}`

**Margens (internas, NAO mostrar ao cliente):**
`{{MARGEM_LUCRO}}`, `{{COMISSAO}}`, `{{IMPOSTO}}`

**Datas:**
`{{DATA_ORCAMENTO}}`, `{{DATA_VALIDADE}}`, `{{DATA_EXTENSO}}`

### Variaveis Template Contrato (28)

**Cliente:** `{{cliente_nome}}`, `{{cliente_cpf_cnpj}}`, `{{cliente_endereco}}`, `{{cliente_bairro}}`, `{{cliente_cidade}}`, `{{cliente_estado}}`, `{{cliente_cep}}`

**Empresa (do Tenant):** `{{empresa_razao_social}}`, `{{empresa_cnpj}}`, `{{empresa_endereco}}`, `{{empresa_cidade}}`, `{{empresa_cep}}`, `{{empresa_representante_nome}}`, `{{empresa_representante_cpf}}`, `{{empresa_representante_rg}}`

**Banco:** `{{banco_nome}}`, `{{banco_agencia}}`, `{{banco_conta}}`, `{{banco_titular}}`

**Equipamento/Valores:** `{{potencia_total}}`, `{{quantidade_paineis}}`, `{{valor_total}}`, `{{valor_total_extenso}}`, `{{numero_parcelas}}`, `{{valor_parcela}}`, `{{valor_parcela_extenso}}`

**Termos:** `{{prazo_execucao_dias}}`, `{{garantia_instalacao_meses}}`, `{{foro_comarca}}`

---

## 5. Vendedores e Comissoes

```
Tipos: vendedor | indicacao
Comissao = valor_venda * (comissao_percentual / 100)
Vendedor bloqueado: nao pode logar nem criar orcamentos
```

### Permissoes
- **Admin/Staff**: Ve tudo
- **Vendedor**: Ve apenas seus proprios clientes e orcamentos
- **Indicacao**: Ve apenas clientes indicados

---

## 6. Multi-Tenancy (WhiteLabel)

### Modelo Tenant
```
Tenant:
  - id (UUID)
  - nome_fantasia
  - razao_social
  - cnpj
  - endereco, cidade, estado, cep
  - representante_nome, representante_cpf, representante_rg
  - banco_nome, banco_agencia, banco_conta, banco_titular
  - logo_url
  - cor_primaria, cor_secundaria
  - dominio_customizado (ex: app.mabenergia.com.br)
  - plano (free, pro, enterprise)
  - ativo
```

### Isolamento
- Toda query filtra por `tenant_id`
- JWT contem `tenant_id`
- Middleware injeta tenant em toda request
- NUNCA expor dados entre tenants
