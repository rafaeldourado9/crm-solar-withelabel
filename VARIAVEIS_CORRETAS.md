# 📝 VARIÁVEIS CORRETAS PARA O TEMPLATE

## ❌ Problemas Encontrados no Seu Template

Seu template atual usa variáveis INCORRETAS:
- `{{CLIENTE_NOME}}` ❌ → Deveria ser `{{NOME_CLIENTE}}` ✅
- `{{POTENCIA_TOTAL_KWP}}` ❌ → Deveria ser `{{POTENCIA_KWP}}` ✅

## ✅ Lista Completa de Variáveis Corretas

### 📋 Orçamento
```
{{NUMERO_ORCAMENTO}}      - Ex: ORC-0001
{{DATA_ORCAMENTO}}        - Ex: 02/02/2025
{{DATA_VALIDADE}}         - Ex: 17/02/2025
```

### 👤 Cliente
```
{{NOME_CLIENTE}}          - Nome do cliente
{{CPF_CNPJ}}              - CPF ou CNPJ
{{TELEFONE}}              - Telefone
{{EMAIL}}                 - E-mail
{{ENDERECO}}              - Endereço completo
{{CIDADE}}                - Cidade
{{ESTADO}}                - Estado (sigla)
```

### ⚡ Sistema
```
{{POTENCIA_KWP}}          - Ex: 5.40 (potência em kWp)
{{GERACAO_MENSAL}}        - Ex: 648 (geração mensal em kWh)
{{GERACAO_ANUAL}}         - Ex: 7776 (geração anual em kWh)
```

### 🔧 Equipamentos
```
{{MARCA_PAINEL}}          - Ex: Canadian Solar
{{POTENCIA_PAINEL}}       - Ex: 450 (potência em W)
{{QUANTIDADE_PAINEIS}}    - Ex: 12
{{MARCA_INVERSOR}}        - Ex: Growatt
{{POTENCIA_INVERSOR}}     - Ex: 5000 (potência em W)
{{POTENCIA_INVERSOR_KW}}  - Ex: 5.0 (potência em kW)
{{QUANTIDADE_INVERSORES}} - Ex: 1
{{TIPO_ESTRUTURA}}        - Ex: Fibrocimento
```

### 💰 Valores (já formatados em R$)
```
{{VALOR_KIT}}             - Ex: R$ 15.000,00
{{VALOR_ESTRUTURA}}       - Ex: R$ 2.500,00
{{VALOR_MATERIAL_ELETRICO}} - Ex: R$ 1.200,00
{{VALOR_PROJETO}}         - Ex: R$ 800,00
{{VALOR_MONTAGEM}}        - Ex: R$ 3.600,00
{{VALOR_TOTAL}}           - Ex: R$ 23.100,00
{{VALOR_FINAL}}           - Ex: R$ 28.000,00
```

### 💳 Pagamento
```
{{FORMA_PAGAMENTO}}       - Ex: "À vista" ou "12x de R$ 2.500,00"
{{TAXA_JUROS}}            - Ex: 2.50%
```

### 👨‍💼 Vendedor
```
{{NOME_VENDEDOR}}         - Nome do vendedor
{{TELEFONE_VENDEDOR}}     - Telefone do vendedor
{{EMAIL_VENDEDOR}}        - E-mail do vendedor
```

### 📊 Premissas
```
{{HSP}}                   - Ex: 4.50 (Horas de Sol Pico)
{{PERDA_SISTEMA}}         - Ex: 20.0% (Perda do sistema)
```

## 🔧 Como Corrigir Seu Template

### Opção 1: Editar o Template Existente

1. Baixe o template atual do admin
2. Abra no Word
3. Substitua:
   - `{{CLIENTE_NOME}}` → `{{NOME_CLIENTE}}`
   - `{{POTENCIA_TOTAL_KWP}}` → `{{POTENCIA_KWP}}`
4. Adicione outras variáveis que desejar da lista acima
5. Salve o arquivo
6. Faça upload novamente no admin

### Opção 2: Criar Template Novo

Crie um novo arquivo Word com este exemplo:

```
═══════════════════════════════════════════════════════
                    ORÇAMENTO SOLAR
═══════════════════════════════════════════════════════

Orçamento Nº: {{NUMERO_ORCAMENTO}}
Data: {{DATA_ORCAMENTO}}
Validade: {{DATA_VALIDADE}}

─────────────────────────────────────────────────────────
DADOS DO CLIENTE
─────────────────────────────────────────────────────────

Nome: {{NOME_CLIENTE}}
CPF/CNPJ: {{CPF_CNPJ}}
Telefone: {{TELEFONE}}
E-mail: {{EMAIL}}
Cidade: {{CIDADE}} - {{ESTADO}}

─────────────────────────────────────────────────────────
SISTEMA FOTOVOLTAICO
─────────────────────────────────────────────────────────

Potência do Sistema: {{POTENCIA_KWP}} kWp
Geração Mensal Estimada: {{GERACAO_MENSAL}} kWh
Geração Anual Estimada: {{GERACAO_ANUAL}} kWh

─────────────────────────────────────────────────────────
EQUIPAMENTOS
─────────────────────────────────────────────────────────

Painéis Solares: {{QUANTIDADE_PAINEIS}}x {{MARCA_PAINEL}} {{POTENCIA_PAINEL}}W
Inversor: {{QUANTIDADE_INVERSORES}}x {{MARCA_INVERSOR}} {{POTENCIA_INVERSOR_KW}} kW
Estrutura: {{TIPO_ESTRUTURA}}

─────────────────────────────────────────────────────────
COMPOSIÇÃO DE VALORES
─────────────────────────────────────────────────────────

Valor do Kit: {{VALOR_KIT}}
Estrutura: {{VALOR_ESTRUTURA}}
Material Elétrico: {{VALOR_MATERIAL_ELETRICO}}
Projeto: {{VALOR_PROJETO}}
Montagem: {{VALOR_MONTAGEM}}

═══════════════════════════════════════════════════════
VALOR TOTAL: {{VALOR_TOTAL}}
VALOR FINAL: {{VALOR_FINAL}}
═══════════════════════════════════════════════════════

FORMA DE PAGAMENTO
{{FORMA_PAGAMENTO}}

─────────────────────────────────────────────────────────
INFORMAÇÕES DO VENDEDOR
─────────────────────────────────────────────────────────

{{NOME_VENDEDOR}}
Telefone: {{TELEFONE_VENDEDOR}}
E-mail: {{EMAIL_VENDEDOR}}
```

## ⚠️ Regras Importantes

1. **Use MAIÚSCULAS**: `{{NOME_CLIENTE}}` ✅ não `{{nome_cliente}}` ❌
2. **Use duas chaves**: `{{VARIAVEL}}` ✅ não `{VARIAVEL}` ❌
3. **Sem espaços**: `{{NOME}}` ✅ não `{{ NOME }}` ❌
4. **Exatamente como na lista**: Copie e cole as variáveis desta lista

## 🧪 Testar

Depois de corrigir o template:

1. Faça upload no admin
2. Marque como "Ativo"
3. Vá para um orçamento
4. Clique em "Gerar PDF"
5. Abra o arquivo baixado
6. Verifique se os dados foram preenchidos corretamente

Se ainda aparecer `{{NOME_CLIENTE}}` no arquivo gerado, significa que a variável está escrita errada no template!
