# ✅ VARIÁVEIS SUPORTADAS NO TEMPLATE

## 🎉 Seu Template Agora Funciona!

As variáveis que você está usando agora são suportadas:
- ✅ `{{CLIENTE_NOME}}` - Funciona!
- ✅ `{{POTENCIA_TOTAL_KWP}}` - Funciona!

## 📋 Lista Completa de Variáveis

### 👤 Cliente
```
{{NOME_CLIENTE}}          - Nome do cliente
{{CLIENTE_NOME}}          - Nome do cliente (alias)
{{CPF_CNPJ}}              - CPF ou CNPJ
{{TELEFONE}}              - Telefone
{{EMAIL}}                 - E-mail
{{ENDERECO}}              - Endereço completo
{{CIDADE}}                - Cidade
{{ESTADO}}                - Estado
```

### ⚡ Sistema
```
{{POTENCIA_KWP}}          - Potência em kWp (ex: 5.40)
{{POTENCIA_TOTAL_KWP}}    - Potência em kWp (alias)
{{GERACAO_MENSAL}}        - Geração mensal em kWh
{{GERACAO_ANUAL}}         - Geração anual em kWh
```

### 🔧 Equipamentos
```
{{MARCA_PAINEL}}          - Marca do painel
{{POTENCIA_PAINEL}}       - Potência do painel em W
{{QUANTIDADE_PAINEIS}}    - Quantidade de painéis
{{MARCA_INVERSOR}}        - Marca do inversor
{{POTENCIA_INVERSOR}}     - Potência do inversor em W
{{POTENCIA_INVERSOR_KW}}  - Potência do inversor em kW
{{QUANTIDADE_INVERSORES}} - Quantidade de inversores
{{TIPO_ESTRUTURA}}        - Tipo de estrutura
```

### 💰 Valores (formatados em R$)
```
{{VALOR_KIT}}             - Valor do kit
{{VALOR_ESTRUTURA}}       - Valor da estrutura
{{VALOR_MATERIAL_ELETRICO}} - Valor do material elétrico
{{VALOR_PROJETO}}         - Valor do projeto
{{VALOR_MONTAGEM}}        - Valor da montagem
{{VALOR_TOTAL}}           - Valor total
{{VALOR_FINAL}}           - Valor final
```

### 📋 Orçamento
```
{{NUMERO_ORCAMENTO}}      - Número do orçamento (ex: ORC-0001)
{{DATA_ORCAMENTO}}        - Data de criação (DD/MM/YYYY)
{{DATA_VALIDADE}}         - Data de validade (DD/MM/YYYY)
```

### 💳 Pagamento
```
{{FORMA_PAGAMENTO}}       - Forma de pagamento
{{TAXA_JUROS}}            - Taxa de juros
```

### 👨💼 Vendedor
```
{{NOME_VENDEDOR}}         - Nome do vendedor
{{TELEFONE_VENDEDOR}}     - Telefone do vendedor
{{EMAIL_VENDEDOR}}        - E-mail do vendedor
```

### 📊 Premissas
```
{{HSP}}                   - Horas de Sol Pico
{{PERDA_SISTEMA}}         - Perda do sistema em %
```

## 🧪 Testar Agora

1. Acesse: http://localhost:5173/orcamentos
2. Clique em um orçamento
3. Clique em **"Gerar PDF"**
4. Abra o arquivo baixado
5. ✅ Os dados devem estar preenchidos corretamente!

## 📝 Observações

- Todas as variáveis devem usar `{{` e `}}`
- As variáveis são case-sensitive (MAIÚSCULAS)
- Você pode usar tanto `{{NOME_CLIENTE}}` quanto `{{CLIENTE_NOME}}`
- Você pode usar tanto `{{POTENCIA_KWP}}` quanto `{{POTENCIA_TOTAL_KWP}}`
