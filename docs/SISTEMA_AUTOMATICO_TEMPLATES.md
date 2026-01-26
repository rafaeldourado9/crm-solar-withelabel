# Sistema Automático de Preenchimento de Templates

## Como Funciona

O sistema agora preenche automaticamente seus documentos Word com os dados reais do orçamento!

## Passo a Passo

### 1. Prepare seu Template Word

Abra seu documento Word (proposta ou contrato) e substitua os campos dinâmicos pelas chaves:

**Antes:**
```
Cliente: João da Silva
CPF: 123.456.789-00
Cidade: Dourados/MS
```

**Depois:**
```
Cliente: {{CLIENTE_NOME}}
CPF: {{CLIENTE_CPF_CNPJ}}
Cidade: {{CLIENTE_CIDADE}}/{{CLIENTE_ESTADO}}
```

### 2. Faça Upload do Template

1. Acesse **Templates** no menu
2. Clique em **Novo Template**
3. Preencha:
   - Nome: "Proposta Comercial Padrão"
   - Tipo: Orçamento
   - Arquivo: Seu .docx com as chaves
4. Clique em **Enviar**

### 3. Gere o Documento

1. Acesse um orçamento
2. Clique em **Gerar PDF Dimensionamento**
3. O sistema:
   - Pega o template ativo
   - Substitui TODAS as chaves automaticamente
   - Gera um .docx pronto para usar

## Chaves Disponíveis

### Cliente
- `{{CLIENTE_NOME}}` - Nome completo
- `{{CLIENTE_CPF_CNPJ}}` - CPF ou CNPJ
- `{{CLIENTE_TELEFONE}}` - Telefone
- `{{CLIENTE_EMAIL}}` - Email
- `{{CLIENTE_ENDERECO}}` - Endereço
- `{{CLIENTE_BAIRRO}}` - Bairro
- `{{CLIENTE_CIDADE}}` - Cidade
- `{{CLIENTE_ESTADO}}` - UF
- `{{CLIENTE_CEP}}` - CEP

### Sistema
- `{{PAINEIS_QTD}}` - Quantidade de painéis
- `{{PAINEIS_MARCA}}` - Marca dos painéis
- `{{PAINEIS_POTENCIA}}` - Potência unitária (W)
- `{{INVERSOR_QTD}}` - Quantidade de inversores
- `{{INVERSOR_MARCA}}` - Marca do inversor
- `{{INVERSOR_POTENCIA}}` - Potência do inversor (W)
- `{{POTENCIA_TOTAL_KWP}}` - Potência total (kWp)
- `{{TIPO_ESTRUTURA}}` - Tipo de estrutura

### Geração
- `{{GERACAO_ESTIMADA_KWH}}` - Geração mensal (kWh)
- `{{GERACAO_ANUAL_KWH}}` - Geração anual (kWh)
- `{{HSP}}` - Horas de Sol Pleno
- `{{PERDA_SISTEMA}}` - Perda do sistema (%)

### Valores
- `{{VALOR_KIT}}` - Valor do kit
- `{{VALOR_PROJETO}}` - Valor do projeto
- `{{VALOR_MONTAGEM}}` - Valor da montagem
- `{{VALOR_ESTRUTURA}}` - Valor da estrutura
- `{{VALOR_MATERIAL_ELETRICO}}` - Material elétrico
- `{{CUSTO_TOTAL}}` - Custo total
- `{{VALOR_FINAL}}` - Valor final

### Pagamento
- `{{FORMA_PAGAMENTO}}` - Forma de pagamento
- `{{NUMERO_PARCELAS}}` - Número de parcelas
- `{{VALOR_PARCELA}}` - Valor da parcela
- `{{TAXA_JUROS}}` - Taxa de juros (%)

### Análise
- `{{ECONOMIA_MENSAL}}` - Economia mensal (R$)
- `{{PAYBACK_ANOS}}` - Payback em anos
- `{{TARIFA_ENERGIA}}` - Tarifa de energia (R$/kWh)

### Outros
- `{{NUMERO_ORCAMENTO}}` - Número do orçamento
- `{{DATA_CRIACAO}}` - Data de criação
- `{{NOME_KIT}}` - Nome do kit
- `{{VALIDADE_PROPOSTA_DIAS}}` - Validade em dias
- `{{PRAZO_ENTREGA}}` - Prazo de entrega
- `{{GARANTIA_INSTALACAO}}` - Garantia (meses)
- `{{VENDEDOR_NOME}}` - Nome do vendedor
- `{{VENDEDOR_TELEFONE}}` - Telefone do vendedor
- `{{VENDEDOR_EMAIL}}` - Email do vendedor

## Exemplo Prático

### Template Word Original:
```
PROPOSTA COMERCIAL Nº {{NUMERO_ORCAMENTO}}

Cliente: {{CLIENTE_NOME}}
CPF/CNPJ: {{CLIENTE_CPF_CNPJ}}
Cidade: {{CLIENTE_CIDADE}}/{{CLIENTE_ESTADO}}

SISTEMA FOTOVOLTAICO
- Painéis: {{PAINEIS_QTD}}x {{PAINEIS_MARCA}} {{PAINEIS_POTENCIA}}W
- Inversor: {{INVERSOR_QTD}}x {{INVERSOR_MARCA}} {{INVERSOR_POTENCIA}}W
- Potência Total: {{POTENCIA_TOTAL_KWP}} kWp

VALORES
Investimento Total: R$ {{VALOR_FINAL}}
Forma de Pagamento: {{FORMA_PAGAMENTO}}
Parcelas: {{NUMERO_PARCELAS}}x de R$ {{VALOR_PARCELA}}

ANÁLISE
Geração Mensal: {{GERACAO_ESTIMADA_KWH}} kWh
Economia Mensal: R$ {{ECONOMIA_MENSAL}}
Payback: {{PAYBACK_ANOS}} anos
```

### Documento Gerado:
```
PROPOSTA COMERCIAL Nº ORC-0001

Cliente: João da Silva
CPF/CNPJ: 123.456.789-00
Cidade: Dourados/MS

SISTEMA FOTOVOLTAICO
- Painéis: 11x OSDA 550W
- Inversor: 1x Solis 5000W
- Potência Total: 6.05 kWp

VALORES
Investimento Total: R$ 16.300,00
Forma de Pagamento: 12x
Parcelas: 12x de R$ 1.358,33

ANÁLISE
Geração Mensal: 726 kWh
Economia Mensal: R$ 580,80
Payback: 2.3 anos
```

## Vantagens

✅ **Automático** - Sem digitação manual
✅ **Sem Erros** - Dados sempre corretos
✅ **Rápido** - Gera em segundos
✅ **Personalizado** - Use seu layout
✅ **Profissional** - Mantém formatação

## Dicas

1. **Mantenha a formatação** - As chaves herdam a formatação do texto
2. **Use em tabelas** - Funciona em células de tabela
3. **Teste primeiro** - Gere um documento de teste antes
4. **Backup** - Guarde uma cópia do template original
5. **Múltiplos templates** - Crie templates diferentes para cada situação

## Requisitos

```bash
pip install python-docx
```

Já está instalado no Docker!
