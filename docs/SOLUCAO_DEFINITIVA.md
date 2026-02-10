# ⚡ SOLUÇÃO DEFINITIVA - Erro 404 ao Gerar PDF

## 🎯 Causa do Erro 404

O endpoint `/api/orcamentos/{id}/gerar-pdf-dimensionamento/` **existe e está correto**, mas retorna 404 porque:

```python
# backend/apps/orcamentos/views.py (linha ~195)
template = Template.objects.filter(tipo='orcamento', ativo=True).first()

if not template:
    return Response({'error': 'Nenhum template de orçamento ativo encontrado'}, status=404)
```

**Não há template cadastrado no banco de dados.**

## ✅ Solução em 1 Comando

```bash
cd backend
python resolver_erro_pdf.py
```

Este script:
1. Verifica/instala python-docx
2. Cria template DOCX automaticamente
3. Cadastra no banco de dados
4. Testa a geração
5. ✅ Resolve o problema!

## 🧪 Testar

Após executar o script:

1. Acesse: http://localhost:5173/orcamentos
2. Clique em um orçamento
3. Clique em **"Gerar PDF"**
4. ✅ Arquivo `.docx` baixa automaticamente!

## 📝 O que o Frontend está fazendo (CORRETO)

```javascript
// frontend/src/pages/OrcamentoDetalhe.jsx (linha 193)
const response = await api.get(`/orcamentos/${id}/gerar-pdf-dimensionamento/`, {
  responseType: 'blob'
});
```

✅ A chamada está **correta**
✅ O endpoint **existe**
✅ O problema é **falta de template no banco**

## 🔍 Verificar se Template Existe

```bash
cd backend
python manage.py shell
```

```python
from apps.templates.models import Template
templates = Template.objects.filter(tipo='orcamento', ativo=True)
print(f"Templates ativos: {templates.count()}")
```

Se retornar `0`, execute: `python resolver_erro_pdf.py`

## 📚 Resumo Técnico

| Item | Status | Observação |
|------|--------|------------|
| Frontend | ✅ Correto | Chama `/orcamentos/{id}/gerar-pdf-dimensionamento/` |
| Backend Endpoint | ✅ Existe | Rota configurada com `url_path='gerar-pdf-dimensionamento'` |
| Backend View | ✅ Correto | Função `gerar_pdf_dimensionamento` implementada |
| Template no Banco | ❌ Falta | Nenhum template cadastrado |
| python-docx | ✅ Instalado | Presente no requirements.txt |

**Solução:** Cadastrar template no banco executando `python resolver_erro_pdf.py`
