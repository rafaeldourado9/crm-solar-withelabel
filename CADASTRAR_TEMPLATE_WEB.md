# 📝 Como Cadastrar Template de Orçamento (Via Interface Web)

## 🎯 Solução para Erro 404 ao Gerar PDF

O erro ocorre porque não há template cadastrado. Siga estes passos:

## 📋 Passo 1: Criar Arquivo DOCX

Abra o Microsoft Word (ou LibreOffice Writer) e crie um documento com este conteúdo:

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

**Salve como:** `template_orcamento.docx`

## 📤 Passo 2: Fazer Upload no Sistema

1. Acesse o admin Django: **http://localhost:8000/admin/**

2. Faça login com suas credenciais de superusuário

3. No menu lateral, clique em **"Templates"** → **"Templates"**

4. Clique no botão **"ADICIONAR TEMPLATE"** (canto superior direito)

5. Preencha o formulário:
   - **Nome:** `Orçamento Padrão`
   - **Tipo:** Selecione **"Orçamento"** no dropdown
   - **Arquivo:** Clique em "Escolher arquivo" e selecione o `template_orcamento.docx`
   - **Arquivo nome:** `template_orcamento.docx`
   - **Ativo:** ✓ Marque esta caixa

6. Clique em **"SALVAR"**

## ✅ Passo 3: Testar

1. Volte para a aplicação: **http://localhost:5173**

2. Vá para **Orçamentos**

3. Clique em um orçamento para ver os detalhes

4. Clique no botão **"Gerar PDF"**

5. ✅ O arquivo PDF será baixado automaticamente!

## 🔄 Atualizar Docker (Necessário)

Para que a conversão DOCX → PDF funcione, você precisa atualizar o container:

```bash
# 1. Parar os containers
docker-compose down

# 2. Reconstruir o backend com as novas dependências
docker-compose build backend

# 3. Subir novamente
docker-compose up -d
```

## 📝 Variáveis Disponíveis

Use estas variáveis no seu template DOCX (sempre com `{{` e `}}`):

### Cliente
- `{{NOME_CLIENTE}}` - Nome do cliente
- `{{CPF_CNPJ}}` - CPF ou CNPJ
- `{{TELEFONE}}` - Telefone
- `{{EMAIL}}` - E-mail
- `{{ENDERECO}}` - Endereço completo
- `{{CIDADE}}` - Cidade
- `{{ESTADO}}` - Estado

### Orçamento
- `{{NUMERO_ORCAMENTO}}` - Ex: ORC-0001
- `{{DATA_ORCAMENTO}}` - Data de criação (DD/MM/YYYY)
- `{{DATA_VALIDADE}}` - Data de validade (DD/MM/YYYY)

### Sistema
- `{{POTENCIA_KWP}}` - Potência em kWp (ex: 5.40)
- `{{GERACAO_MENSAL}}` - Geração mensal em kWh
- `{{GERACAO_ANUAL}}` - Geração anual em kWh

### Equipamentos
- `{{MARCA_PAINEL}}` - Marca do painel
- `{{POTENCIA_PAINEL}}` - Potência do painel em W
- `{{QUANTIDADE_PAINEIS}}` - Quantidade de painéis
- `{{MARCA_INVERSOR}}` - Marca do inversor
- `{{POTENCIA_INVERSOR_KW}}` - Potência do inversor em kW
- `{{QUANTIDADE_INVERSORES}}` - Quantidade de inversores
- `{{TIPO_ESTRUTURA}}` - Tipo de estrutura

### Valores (já formatados em R$)
- `{{VALOR_KIT}}` - Valor do kit
- `{{VALOR_ESTRUTURA}}` - Valor da estrutura
- `{{VALOR_MATERIAL_ELETRICO}}` - Valor do material elétrico
- `{{VALOR_PROJETO}}` - Valor do projeto
- `{{VALOR_MONTAGEM}}` - Valor da montagem
- `{{VALOR_TOTAL}}` - Valor total
- `{{VALOR_FINAL}}` - Valor final

### Pagamento
- `{{FORMA_PAGAMENTO}}` - Ex: "À vista" ou "12x de R$ 2.500,00"
- `{{TAXA_JUROS}}` - Taxa de juros aplicada

### Vendedor
- `{{NOME_VENDEDOR}}` - Nome do vendedor
- `{{TELEFONE_VENDEDOR}}` - Telefone do vendedor
- `{{EMAIL_VENDEDOR}}` - E-mail do vendedor

## 🎨 Dicas de Formatação

- Use **negrito** para destacar títulos
- Use cores para diferenciar seções
- Adicione tabelas para organizar valores
- Insira logo da empresa no cabeçalho
- Personalize fontes e espaçamentos

## ⚠️ Importante

- As variáveis devem estar EXATAMENTE como mostrado: `{{VARIAVEL}}`
- Use MAIÚSCULAS
- Use duas chaves de cada lado: `{{` e `}}`
- Não adicione espaços: ❌ `{{ VARIAVEL }}` ✅ `{{VARIAVEL}}`

## 🆘 Problemas?

### Erro: "Nenhum template de orçamento ativo encontrado"
- Verifique se marcou a caixa **"Ativo"**
- Verifique se selecionou **"Orçamento"** no campo Tipo

### Arquivo não baixa
- Verifique se reconstruiu o Docker: `docker-compose build backend`
- Verifique os logs: `docker-compose logs backend`

### Variáveis não são substituídas
- Verifique se usou `{{VARIAVEL}}` (maiúsculas, duas chaves)
- Verifique se não há espaços dentro das chaves
