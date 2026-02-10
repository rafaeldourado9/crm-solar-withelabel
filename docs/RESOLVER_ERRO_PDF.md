# ⚡ SOLUÇÃO EM 1 COMANDO - Erro 404 ao Gerar PDF

## 🎯 Problema
```
AxiosError: Request failed with status code 404
```
Ao clicar em "Gerar PDF" no orçamento.

## ✅ Causa
Nenhum template de orçamento cadastrado no banco de dados.

## 🚀 Solução Automática

Execute este comando:

```bash
cd backend
python resolver_erro_pdf.py
```

**Pronto!** O script irá:
1. ✓ Verificar python-docx (instala se necessário)
2. ✓ Criar template DOCX com todas as variáveis
3. ✓ Cadastrar automaticamente no banco
4. ✓ Testar a geração
5. ✓ Confirmar que está funcionando

## 🧪 Testar

Após executar o script:

1. Acesse: http://localhost:5173/orcamentos
2. Clique em um orçamento
3. Clique em **"Gerar PDF"**
4. ✅ Arquivo baixa automaticamente!

## 📝 Personalizar Template

Se quiser customizar o template:

1. Acesse: http://localhost:8000/admin/templates/template/
2. Clique no template "Orçamento Padrão (Auto)"
3. Faça upload de um novo arquivo .docx
4. Salve

## 🔧 Solução Manual (se preferir)

### 1. Criar template
```bash
cd backend
python criar_template_exemplo.py
```

### 2. Cadastrar no admin
1. Acesse: http://localhost:8000/admin/templates/template/
2. Adicionar Template
3. Upload do arquivo `template_orcamento_exemplo.docx`
4. Tipo: **Orçamento**
5. Ativo: ✓
6. Salvar

## 📋 Variáveis Disponíveis

Use no seu template .docx:

```
{{NUMERO_ORCAMENTO}}      - Número do orçamento
{{DATA_ORCAMENTO}}        - Data de criação
{{NOME_CLIENTE}}          - Nome do cliente
{{CPF_CNPJ}}              - CPF/CNPJ
{{TELEFONE}}              - Telefone
{{POTENCIA_KWP}}          - Potência em kWp
{{GERACAO_MENSAL}}        - Geração mensal em kWh
{{QUANTIDADE_PAINEIS}}    - Quantidade de painéis
{{MARCA_PAINEL}}          - Marca do painel
{{POTENCIA_PAINEL}}       - Potência do painel
{{MARCA_INVERSOR}}        - Marca do inversor
{{TIPO_ESTRUTURA}}        - Tipo de estrutura
{{VALOR_KIT}}             - Valor do kit (R$ formatado)
{{VALOR_FINAL}}           - Valor final (R$ formatado)
{{FORMA_PAGAMENTO}}       - Forma de pagamento
{{NOME_VENDEDOR}}         - Nome do vendedor
```

Lista completa: `docs/VARIAVEIS_TEMPLATE_ORCAMENTO.md`

## 🆘 Ainda com Problema?

Execute o diagnóstico:

```bash
cd backend
python diagnostico_pdf.py
```

Isso mostrará exatamente onde está o erro.

## 📚 Documentação Completa

- `SOLUCAO_COMPLETA_PDF.md` - Guia detalhado
- `docs/GERACAO_ORCAMENTO.md` - Como usar templates
- `docs/VARIAVEIS_TEMPLATE_ORCAMENTO.md` - Todas as variáveis

---

**Tempo estimado:** 30 segundos ⚡
