# Solução: Erro 404 ao Gerar PDF do Orçamento

## 🔍 Problema Identificado

Erro 404 ao clicar em "Gerar PDF" na página de detalhes do orçamento.

## ✅ Causas Possíveis

1. **Biblioteca python-docx não instalada**
2. **Nenhum template de orçamento cadastrado**
3. **Arquivo de template não existe no servidor**
4. **Erro na importação do serviço**

## 🛠️ Solução Passo a Passo

### 1. Executar Diagnóstico

```bash
cd backend
python diagnostico_pdf.py
```

Este script irá verificar:
- ✓ Se python-docx está instalado
- ✓ Se há templates cadastrados
- ✓ Se os arquivos existem
- ✓ Se a geração funciona

### 2. Instalar Dependências (se necessário)

```bash
cd backend
pip install python-docx
```

### 3. Cadastrar Template

Se não houver template cadastrado:

1. Acesse: http://localhost:8000/admin/templates/template/
2. Clique em "Adicionar Template"
3. Preencha:
   - **Nome:** Orçamento Padrão
   - **Tipo:** Orçamento
   - **Arquivo:** Faça upload de um arquivo .docx
   - **Ativo:** ✓ Marcado
4. Salve

### 4. Criar Template DOCX

Crie um arquivo Word com as variáveis:

```
ORÇAMENTO Nº {{NUMERO_ORCAMENTO}}
Data: {{DATA_ORCAMENTO}}

Cliente: {{NOME_CLIENTE}}
CPF/CNPJ: {{CPF_CNPJ}}
Telefone: {{TELEFONE}}

SISTEMA FOTOVOLTAICO
Potência: {{POTENCIA_KWP}} kWp
Geração Mensal: {{GERACAO_MENSAL}} kWh

EQUIPAMENTOS
Painéis: {{QUANTIDADE_PAINEIS}}x {{MARCA_PAINEL}} {{POTENCIA_PAINEL}}W
Inversor: {{QUANTIDADE_INVERSORES}}x {{MARCA_INVERSOR}} {{POTENCIA_INVERSOR}}W
Estrutura: {{TIPO_ESTRUTURA}}

VALORES
Valor do Kit: {{VALOR_KIT}}
Estrutura: {{VALOR_ESTRUTURA}}
Material Elétrico: {{VALOR_MATERIAL_ELETRICO}}
Projeto: {{VALOR_PROJETO}}
Montagem: {{VALOR_MONTAGEM}}

VALOR TOTAL: {{VALOR_TOTAL}}
VALOR FINAL: {{VALOR_FINAL}}

Forma de Pagamento: {{FORMA_PAGAMENTO}}
```

Salve como `template_orcamento.docx` e faça upload no admin.

### 5. Verificar Logs do Backend

Se o erro persistir, verifique os logs:

```bash
docker-compose logs backend
```

Procure por erros relacionados a:
- ImportError
- FileNotFoundError
- Template.DoesNotExist

## 🔧 Correção Alternativa

Se o problema for no endpoint, verifique se a URL está correta:

**URL Correta:**
```
GET /api/orcamentos/{id}/gerar-pdf-dimensionamento/
```

**Exemplo:**
```
http://localhost:8000/api/orcamentos/1/gerar-pdf-dimensionamento/
```

## 📝 Variáveis Disponíveis

Consulte a lista completa em: `docs/VARIAVEIS_TEMPLATE_ORCAMENTO.md`

Principais variáveis:
- `{{NUMERO_ORCAMENTO}}` - Número do orçamento
- `{{NOME_CLIENTE}}` - Nome do cliente
- `{{POTENCIA_KWP}}` - Potência em kWp
- `{{VALOR_FINAL}}` - Valor final formatado
- `{{FORMA_PAGAMENTO}}` - Forma de pagamento

## 🧪 Testar Manualmente

Execute o teste:

```bash
cd backend
python testar_geracao_orcamento.py
```

Isso irá gerar um arquivo `teste_orcamento_XXX.docx` para validação.

## ❓ Ainda com Problemas?

1. Verifique se o Docker está rodando:
   ```bash
   docker-compose ps
   ```

2. Reinicie os containers:
   ```bash
   docker-compose restart backend
   ```

3. Verifique as permissões da pasta media:
   ```bash
   ls -la backend/media/templates/
   ```

4. Consulte os logs detalhados:
   ```bash
   docker-compose logs -f backend
   ```
