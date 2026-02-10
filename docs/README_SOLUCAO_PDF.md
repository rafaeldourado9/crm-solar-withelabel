# ⚡ SOLUÇÃO COMPLETA - Erro 404 ao Gerar PDF

## 🎯 Problema
Erro 404 ao clicar em "Gerar PDF" no orçamento.

## ✅ Causa
Nenhum template cadastrado no banco de dados.

## 🚀 Solução (3 Passos Simples)

### 1️⃣ Criar Template DOCX

Abra o Word e crie um arquivo com este conteúdo mínimo:

```
ORÇAMENTO Nº {{NUMERO_ORCAMENTO}}
Data: {{DATA_ORCAMENTO}}

CLIENTE: {{NOME_CLIENTE}}
CPF/CNPJ: {{CPF_CNPJ}}

SISTEMA: {{POTENCIA_KWP}} kWp
Painéis: {{QUANTIDADE_PAINEIS}}x {{MARCA_PAINEL}} {{POTENCIA_PAINEL}}W
Inversor: {{QUANTIDADE_INVERSORES}}x {{MARCA_INVERSOR}}

VALOR FINAL: {{VALOR_FINAL}}
Pagamento: {{FORMA_PAGAMENTO}}
```

Salve como `template_orcamento.docx`

### 2️⃣ Cadastrar no Sistema

1. Acesse: **http://localhost:8000/admin/**
2. Login com superusuário
3. Menu **Templates** → **Templates**
4. Clique **"ADICIONAR TEMPLATE"**
5. Preencha:
   - Nome: `Orçamento Padrão`
   - Tipo: **Orçamento**
   - Arquivo: Upload do `template_orcamento.docx`
   - Ativo: ✓ Marcar
6. **SALVAR**

### 3️⃣ Atualizar Docker

```bash
docker-compose down
docker-compose build backend
docker-compose up -d
```

## ✅ Testar

1. Acesse: http://localhost:5173/orcamentos
2. Clique em um orçamento
3. Clique **"Gerar PDF"**
4. ✅ Arquivo baixa automaticamente!

## 📝 O Sistema Agora:

1. ✅ Pega o template DOCX do banco
2. ✅ Substitui as variáveis `{{VARIAVEL}}`
3. ✅ Tenta converter para PDF
4. ✅ Se falhar, retorna DOCX (funciona igual)

## 📋 Variáveis Principais

- `{{NUMERO_ORCAMENTO}}` - Número do orçamento
- `{{NOME_CLIENTE}}` - Nome do cliente
- `{{POTENCIA_KWP}}` - Potência em kWp
- `{{QUANTIDADE_PAINEIS}}` - Quantidade de painéis
- `{{MARCA_PAINEL}}` - Marca do painel
- `{{VALOR_FINAL}}` - Valor final (R$ formatado)
- `{{FORMA_PAGAMENTO}}` - Forma de pagamento

**Lista completa:** Ver `CADASTRAR_TEMPLATE_WEB.md`

## 🎨 Personalize

Você pode:
- Adicionar logo da empresa
- Mudar cores e fontes
- Adicionar tabelas
- Incluir mais informações
- Usar qualquer variável da lista

## 📚 Documentos Criados

- **`CADASTRAR_TEMPLATE_WEB.md`** - Guia completo com todas as variáveis
- **`ATUALIZAR_DOCKER.md`** - Como atualizar o Docker
- Este arquivo - Resumo rápido

## ⚠️ Importante

- Variáveis devem ser MAIÚSCULAS: `{{VARIAVEL}}`
- Use duas chaves: `{{` e `}}`
- Sem espaços: ✅ `{{NOME}}` ❌ `{{ NOME }}`
- Template deve estar marcado como **Ativo**
- Tipo deve ser **Orçamento**

---

**Tempo total:** 5 minutos ⚡
