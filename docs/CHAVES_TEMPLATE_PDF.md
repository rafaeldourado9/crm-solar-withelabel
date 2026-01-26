# Chaves para Template PDF de Dimensionamento

## Como usar
Substitua estas chaves no seu template HTML/PDF para gerar documentos personalizados.

## Chaves Disponíveis

### Dados do Orçamento
- `{{NUMERO_ORCAMENTO}}` - Número do orçamento (ex: ORC-0001)
- `{{DATA_CRIACAO}}` - Data de criação do orçamento
- `{{NOME_KIT}}` - Nome do kit (ex: Kit 5kWp Residencial)

### Dados do Cliente
- `{{CLIENTE_NOME}}` - Nome completo do cliente
- `{{CLIENTE_CPF_CNPJ}}` - CPF ou CNPJ do cliente
- `{{CLIENTE_TELEFONE}}` - Telefone do cliente
- `{{CLIENTE_EMAIL}}` - Email do cliente
- `{{CLIENTE_ENDERECO}}` - Endereço completo
- `{{CLIENTE_BAIRRO}}` - Bairro
- `{{CLIENTE_CIDADE}}` - Cidade
- `{{CLIENTE_ESTADO}}` - Estado (UF)
- `{{CLIENTE_CEP}}` - CEP

### Sistema Fotovoltaico - Painéis
- `{{PAINEIS_QTD}}` - Quantidade de painéis
- `{{PAINEIS_MARCA}}` - Marca/Fabricante dos painéis
- `{{PAINEIS_MODELO}}` - Modelo dos painéis
- `{{PAINEIS_POTENCIA}}` - Potência unitária em Watts
- `{{PAINEIS_POTENCIA_TOTAL}}` - Potência total dos painéis em Watts

### Sistema Fotovoltaico - Inversor
- `{{INVERSOR_QTD}}` - Quantidade de inversores
- `{{INVERSOR_MARCA}}` - Marca/Fabricante do inversor
- `{{INVERSOR_MODELO}}` - Modelo do inversor
- `{{INVERSOR_POTENCIA}}` - Potência nominal em Watts
- `{{INVERSOR_POTENCIA_MAXIMA}}` - Potência máxima suportada
- `{{INVERSOR_OVERLOAD}}` - Percentual de overload

### Dimensionamento Técnico
- `{{POTENCIA_TOTAL_KWP}}` - Potência total do sistema em kWp
- `{{GERACAO_ESTIMADA_KWH}}` - Geração mensal estimada em kWh
- `{{GERACAO_ANUAL_KWH}}` - Geração anual estimada em kWh
- `{{HSP}}` - Horas de Sol Pleno (HSP)
- `{{PERDA_SISTEMA}}` - Perda do sistema em %
- `{{TIPO_ESTRUTURA}}` - Tipo de estrutura (Cerâmico, Fibrometal, etc)

### Valores Financeiros
- `{{VALOR_KIT}}` - Valor do kit cotado
- `{{VALOR_PROJETO}}` - Valor do projeto
- `{{VALOR_MONTAGEM}}` - Valor da montagem
- `{{VALOR_ESTRUTURA}}` - Valor da estrutura
- `{{VALOR_MATERIAL_ELETRICO}}` - Valor do material elétrico
- `{{VALOR_DESLOCAMENTO}}` - Valor do deslocamento (se houver)
- `{{CUSTO_TOTAL}}` - Custo total do sistema
- `{{VALOR_BASE}}` - Valor base (antes de margem)
- `{{MARGEM_DESCONTO}}` - Margem de desconto à vista
- `{{VALOR_FINAL}}` - Valor final do orçamento

### Breakdown Financeiro
- `{{COMISSAO_PERCENTUAL}}` - Percentual de comissão
- `{{COMISSAO_VALOR}}` - Valor da comissão em R$
- `{{IMPOSTO_PERCENTUAL}}` - Percentual de imposto
- `{{IMPOSTO_VALOR}}` - Valor do imposto em R$
- `{{LUCRO_PERCENTUAL}}` - Percentual de lucro
- `{{LUCRO_VALOR}}` - Valor do lucro em R$

### Pagamento
- `{{FORMA_PAGAMENTO}}` - Forma de pagamento (À vista, 12x, etc)
- `{{TAXA_JUROS}}` - Taxa de juros aplicada
- `{{NUMERO_PARCELAS}}` - Número de parcelas
- `{{VALOR_PARCELA}}` - Valor de cada parcela

### Premissas Técnicas
- `{{TARIFA_ENERGIA}}` - Tarifa de energia atual (R$/kWh)
- `{{INFLACAO_ENERGETICA}}` - Inflação energética anual (%)
- `{{PERDA_EFICIENCIA_ANUAL}}` - Perda de eficiência anual (%)
- `{{PRAZO_ENTREGA}}` - Prazo de entrega em dias
- `{{GARANTIA_INSTALACAO}}` - Garantia da instalação em meses

### Vendedor (se houver)
- `{{VENDEDOR_NOME}}` - Nome do vendedor
- `{{VENDEDOR_EMAIL}}` - Email do vendedor
- `{{VENDEDOR_TELEFONE}}` - Telefone do vendedor

### Empresa
- `{{EMPRESA_NOME}}` - Nome da empresa
- `{{EMPRESA_CNPJ}}` - CNPJ da empresa
- `{{EMPRESA_ENDERECO}}` - Endereço da empresa
- `{{EMPRESA_TELEFONE}}` - Telefone da empresa
- `{{EMPRESA_EMAIL}}` - Email da empresa
- `{{EMPRESA_SITE}}` - Site da empresa

## Exemplo de Uso

```html
<h1>Orçamento {{NUMERO_ORCAMENTO}}</h1>
<p>Cliente: {{CLIENTE_NOME}}</p>
<p>Sistema: {{PAINEIS_QTD}}x {{PAINEIS_MARCA}} {{PAINEIS_POTENCIA}}W</p>
<p>Potência Total: {{POTENCIA_TOTAL_KWP}} kWp</p>
<p>Geração Estimada: {{GERACAO_ESTIMADA_KWH}} kWh/mês</p>
<p>Valor Final: R$ {{VALOR_FINAL}}</p>
```

## Próximos Passos

1. Criar template HTML personalizado
2. Usar biblioteca como WeasyPrint ou ReportLab para gerar PDF
3. Substituir as chaves pelos valores reais do orçamento
4. Adicionar logotipo e identidade visual da empresa
