# Variáveis Disponíveis para Templates de Orçamento

## Como Usar

No seu template DOCX, use as variáveis no formato `{{NOME_VARIAVEL}}`.

Exemplo: `{{NOME_CLIENTE}}` será substituído pelo nome do cliente.

## Variáveis Disponíveis

### Informações do Orçamento
- `{{NUMERO_ORCAMENTO}}` - Número do orçamento (ex: ORC-0001)
- `{{DATA_ORCAMENTO}}` - Data de criação (formato: DD/MM/YYYY)
- `{{DATA_VALIDADE}}` - Data de validade (formato: DD/MM/YYYY)

### Dados do Cliente
- `{{NOME_CLIENTE}}` - Nome completo do cliente
- `{{CPF_CNPJ}}` - CPF ou CNPJ do cliente
- `{{TELEFONE}}` - Telefone do cliente
- `{{EMAIL}}` - E-mail do cliente
- `{{ENDERECO}}` - Endereço completo
- `{{CIDADE}}` - Cidade
- `{{ESTADO}}` - Estado (UF)

### Sistema Fotovoltaico
- `{{POTENCIA_KWP}}` - Potência total do sistema em kWp (ex: 5.40)
- `{{GERACAO_MENSAL}}` - Geração mensal estimada em kWh (ex: 750)
- `{{GERACAO_ANUAL}}` - Geração anual estimada em kWh (ex: 9000)

### Equipamentos - Painéis
- `{{MARCA_PAINEL}}` - Marca do painel (ex: Canadian Solar)
- `{{POTENCIA_PAINEL}}` - Potência unitária do painel em W (ex: 450)
- `{{QUANTIDADE_PAINEIS}}` - Quantidade de painéis (ex: 12)

### Equipamentos - Inversores
- `{{MARCA_INVERSOR}}` - Marca do inversor (ex: Growatt)
- `{{POTENCIA_INVERSOR}}` - Potência do inversor em W (ex: 5000)
- `{{POTENCIA_INVERSOR_KW}}` - Potência do inversor em kW (ex: 5.0)
- `{{QUANTIDADE_INVERSORES}}` - Quantidade de inversores (ex: 1)

### Estrutura
- `{{TIPO_ESTRUTURA}}` - Tipo de estrutura (ex: Cerâmico/Colonial, Fibrometal, etc)

### Valores Financeiros
- `{{VALOR_KIT}}` - Valor do kit (painéis + inversor) formatado (ex: R$ 15.000,00)
- `{{VALOR_ESTRUTURA}}` - Valor da estrutura formatado
- `{{VALOR_MATERIAL_ELETRICO}}` - Valor dos materiais elétricos formatado
- `{{VALOR_PROJETO}}` - Valor do projeto formatado
- `{{VALOR_MONTAGEM}}` - Valor total da montagem formatado
- `{{VALOR_TOTAL}}` - Custo total (sem margens) formatado
- `{{VALOR_FINAL}}` - Valor final de venda formatado

### Pagamento
- `{{FORMA_PAGAMENTO}}` - Forma de pagamento (ex: À vista, 12x de R$ 1.500,00)
- `{{TAXA_JUROS}}` - Taxa de juros aplicada (ex: 2.50%)

### Vendedor
- `{{NOME_VENDEDOR}}` - Nome do vendedor
- `{{TELEFONE_VENDEDOR}}` - Telefone do vendedor
- `{{EMAIL_VENDEDOR}}` - E-mail do vendedor

### Premissas Técnicas
- `{{HSP}}` - Horas de Sol Pico (ex: 4.50)
- `{{PERDA_SISTEMA}}` - Percentual de perda do sistema (ex: 20.0%)

## Exemplo de Uso no Template

```
PROPOSTA COMERCIAL

Cliente: {{NOME_CLIENTE}}
CPF/CNPJ: {{CPF_CNPJ}}
Telefone: {{TELEFONE}}
E-mail: {{EMAIL}}

SISTEMA FOTOVOLTAICO

Potência: {{POTENCIA_KWP}} kWp
Geração Mensal: {{GERACAO_MENSAL}} kWh
Geração Anual: {{GERACAO_ANUAL}} kWh

EQUIPAMENTOS

Painéis: {{QUANTIDADE_PAINEIS}}x {{MARCA_PAINEL}} {{POTENCIA_PAINEL}}W
Inversor: {{QUANTIDADE_INVERSORES}}x {{MARCA_INVERSOR}} {{POTENCIA_INVERSOR_KW}} kW
Estrutura: {{TIPO_ESTRUTURA}}

VALORES

Valor do Kit: {{VALOR_KIT}}
Estrutura: {{VALOR_ESTRUTURA}}
Material Elétrico: {{VALOR_MATERIAL_ELETRICO}}
Projeto: {{VALOR_PROJETO}}
Montagem: {{VALOR_MONTAGEM}}

VALOR FINAL: {{VALOR_FINAL}}
Forma de Pagamento: {{FORMA_PAGAMENTO}}

Validade: {{DATA_VALIDADE}}
```

## Notas Importantes

1. Todas as variáveis devem estar em MAIÚSCULAS
2. Use exatamente o formato `{{VARIAVEL}}` (com duas chaves de cada lado)
3. Variáveis não encontradas serão mantidas como estão no documento
4. Valores monetários já vêm formatados com R$ e separadores de milhar
5. Datas já vêm formatadas no padrão brasileiro (DD/MM/YYYY)
