# 🚨 SOLUÇÃO RÁPIDA - Erro 404 ao Gerar PDF

## Problema
Erro 404 ao clicar em "Gerar PDF" no orçamento.

## ✅ Causa Confirmada
**Nenhum template de orçamento cadastrado no sistema.**

O endpoint `/api/orcamentos/{id}/gerar-pdf-dimensionamento/` está correto e funcionando, mas retorna 404 porque não encontra nenhum template ativo do tipo "orcamento" no banco de dados.

## ✅ Solução em 3 Passos

### 1️⃣ Execute o Diagnóstico

```bash
cd backend
python diagnostico_pdf.py
```

### 2️⃣ Se não houver template, cadastre um:

**Opção A - Via Admin Django:**
1. Acesse: http://localhost:8000/admin/templates/template/
2. Clique em "Adicionar Template"
3. Preencha:
   - Nome: `Orçamento Padrão`
   - Tipo: `Orçamento`
   - Arquivo: Upload de um .docx
   - Ativo: ✓
4. Salve

**Opção B - Criar Template Básico:**

Crie um arquivo `template_orcamento.docx` com este conteúdo:

```
═══════════════════════════════════════════════════════
                    ORÇAMENTO SOLAR
═══════════════════════════════════════════════════════

Orçamento Nº: {{NUMERO_ORCAMENTO}}
Data: {{DATA_ORCAMENTO}}
Validade: {{DATA_VALIDADE}}

CLIENTE
Nome: {{NOME_CLIENTE}}
CPF/CNPJ: {{CPF_CNPJ}}
Telefone: {{TELEFONE}}
Cidade: {{CIDADE}} - {{ESTADO}}

SISTEMA FOTOVOLTAICO
Potência: {{POTENCIA_KWP}} kWp
Geração Mensal Estimada: {{GERACAO_MENSAL}} kWh
Geração Anual Estimada: {{GERACAO_ANUAL}} kWh

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

───────────────────────────────────────────────────────
VALOR TOTAL: {{VALOR_TOTAL}}
VALOR FINAL: {{VALOR_FINAL}}
───────────────────────────────────────────────────────

FORMA DE PAGAMENTO
{{FORMA_PAGAMENTO}}

VENDEDOR
{{NOME_VENDEDOR}}
{{TELEFONE_VENDEDOR}}
{{EMAIL_VENDEDOR}}
```

Faça upload deste arquivo no admin.

### 3️⃣ Teste Novamente

1. Volte para a página do orçamento
2. Clique em "Gerar PDF"
3. O arquivo deve baixar automaticamente

## 🔍 Verificação Adicional

Se ainda não funcionar, verifique:

```bash
# 1. Verificar se python-docx está instalado
cd backend
pip list | grep python-docx

# 2. Se não estiver, instale:
pip install python-docx

# 3. Reinicie o backend
docker-compose restart backend

# 4. Teste manualmente
python testar_geracao_orcamento.py
```

## 📋 Checklist

- [ ] python-docx instalado
- [ ] Template cadastrado no admin
- [ ] Template marcado como "Ativo"
- [ ] Tipo do template = "Orçamento"
- [ ] Arquivo .docx válido
- [ ] Backend reiniciado

## 🆘 Ainda com Erro?

Execute e envie o resultado:

```bash
cd backend
python diagnostico_pdf.py > diagnostico.txt
cat diagnostico.txt
```

Isso mostrará exatamente onde está o problema.
