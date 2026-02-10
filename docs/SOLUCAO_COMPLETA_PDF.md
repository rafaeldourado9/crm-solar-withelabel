# 🔧 Solução: Erro 404 ao Gerar PDF do Orçamento

## 📌 Resumo do Problema

Ao clicar em "Gerar PDF" na página de detalhes do orçamento, ocorre erro 404:
```
AxiosError: Request failed with status code 404
```

## 🎯 Causa Raiz

O endpoint `/api/orcamentos/{id}/gerar-pdf-dimensionamento/` retorna 404 porque:
- **Nenhum template de orçamento está cadastrado no sistema**

## ✅ Solução Completa

### Passo 1: Verificar o Problema

Execute o diagnóstico:

```bash
cd backend
python diagnostico_pdf.py
```

Este script verifica:
- ✓ Biblioteca python-docx instalada
- ✓ Templates cadastrados
- ✓ Arquivos existem
- ✓ Geração funciona

### Passo 2: Criar Template de Exemplo

Execute o script para criar um template pronto:

```bash
cd backend
python criar_template_exemplo.py
```

Isso criará o arquivo `template_orcamento_exemplo.docx` com todas as variáveis configuradas.

### Passo 3: Cadastrar Template no Sistema

**Opção A - Via Admin Django:**

1. Acesse: http://localhost:8000/admin/templates/template/
2. Faça login com superuser
3. Clique em **"Adicionar Template"**
4. Preencha:
   - **Nome:** `Orçamento Padrão`
   - **Tipo:** `Orçamento` (selecione no dropdown)
   - **Arquivo:** Faça upload do `template_orcamento_exemplo.docx`
   - **Ativo:** ✓ Marque esta opção
5. Clique em **"Salvar"**

**Opção B - Via Django Shell:**

```bash
cd backend
python manage.py shell
```

```python
from apps.templates.models import Template
from django.core.files import File

with open('template_orcamento_exemplo.docx', 'rb') as f:
    template = Template.objects.create(
        nome='Orçamento Padrão',
        tipo='orcamento',
        arquivo=File(f, name='template_orcamento_exemplo.docx'),
        arquivo_nome='template_orcamento_exemplo.docx',
        ativo=True
    )
    print(f"✓ Template criado: {template.id}")
```

### Passo 4: Testar Geração

Execute o teste:

```bash
cd backend
python testar_geracao_orcamento.py
```

Se funcionar, você verá:
```
✅ SUCESSO! Arquivo gerado: teste_orcamento_1.docx
```

### Passo 5: Testar no Frontend

1. Acesse a aplicação: http://localhost:5173
2. Vá para **Orçamentos**
3. Clique em um orçamento para ver detalhes
4. Clique no botão **"Gerar PDF"**
5. O arquivo `.docx` deve baixar automaticamente

## 🔍 Verificações Adicionais

### Se ainda não funcionar:

#### 1. Verificar se python-docx está instalado

```bash
cd backend
pip list | grep python-docx
```

Se não aparecer, instale:

```bash
pip install python-docx
```

#### 2. Verificar templates no banco

```bash
cd backend
python manage.py shell
```

```python
from apps.templates.models import Template
templates = Template.objects.filter(tipo='orcamento', ativo=True)
print(f"Templates ativos: {templates.count()}")
for t in templates:
    print(f"  - {t.nome} | Arquivo: {t.arquivo.name}")
```

#### 3. Verificar logs do backend

```bash
docker-compose logs -f backend
```

Procure por erros como:
- `ImportError: No module named 'docx'`
- `Template.DoesNotExist`
- `FileNotFoundError`

#### 4. Reiniciar containers

```bash
docker-compose restart backend
```

## 📋 Checklist de Verificação

- [ ] python-docx instalado (`pip list | grep python-docx`)
- [ ] Template criado (`python criar_template_exemplo.py`)
- [ ] Template cadastrado no admin
- [ ] Template marcado como "Ativo"
- [ ] Tipo do template = "Orçamento"
- [ ] Arquivo .docx existe e é válido
- [ ] Teste manual funciona (`python testar_geracao_orcamento.py`)
- [ ] Backend reiniciado (`docker-compose restart backend`)
- [ ] Frontend atualizado (F5 no navegador)

## 📝 Variáveis Disponíveis no Template

### Cliente
- `{{NOME_CLIENTE}}` - Nome do cliente
- `{{CPF_CNPJ}}` - CPF ou CNPJ
- `{{TELEFONE}}` - Telefone
- `{{EMAIL}}` - E-mail
- `{{ENDERECO}}` - Endereço completo
- `{{CIDADE}}` - Cidade
- `{{ESTADO}}` - Estado

### Orçamento
- `{{NUMERO_ORCAMENTO}}` - Número do orçamento (ex: ORC-0001)
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
- `{{POTENCIA_INVERSOR}}` - Potência do inversor em W
- `{{POTENCIA_INVERSOR_KW}}` - Potência do inversor em kW
- `{{QUANTIDADE_INVERSORES}}` - Quantidade de inversores
- `{{TIPO_ESTRUTURA}}` - Tipo de estrutura

### Valores
- `{{VALOR_KIT}}` - Valor do kit (R$ formatado)
- `{{VALOR_ESTRUTURA}}` - Valor da estrutura
- `{{VALOR_MATERIAL_ELETRICO}}` - Valor do material elétrico
- `{{VALOR_PROJETO}}` - Valor do projeto
- `{{VALOR_MONTAGEM}}` - Valor da montagem
- `{{VALOR_TOTAL}}` - Valor total
- `{{VALOR_FINAL}}` - Valor final

### Pagamento
- `{{FORMA_PAGAMENTO}}` - Forma de pagamento (ex: "À vista" ou "12x de R$ 2.500,00")
- `{{TAXA_JUROS}}` - Taxa de juros aplicada

### Vendedor
- `{{NOME_VENDEDOR}}` - Nome do vendedor
- `{{TELEFONE_VENDEDOR}}` - Telefone do vendedor
- `{{EMAIL_VENDEDOR}}` - E-mail do vendedor

### Premissas
- `{{HSP}}` - Horas de Sol Pico
- `{{PERDA_SISTEMA}}` - Perda do sistema em %

## 🆘 Suporte

Se o problema persistir após seguir todos os passos:

1. Execute o diagnóstico completo:
   ```bash
   cd backend
   python diagnostico_pdf.py > diagnostico.txt
   cat diagnostico.txt
   ```

2. Verifique os logs:
   ```bash
   docker-compose logs backend | tail -100
   ```

3. Consulte a documentação completa:
   - `docs/GERACAO_ORCAMENTO.md`
   - `docs/VARIAVEIS_TEMPLATE_ORCAMENTO.md`
   - `docs/SISTEMA_AUTOMATICO_TEMPLATES.md`

## 📚 Arquivos Criados

- `backend/diagnostico_pdf.py` - Script de diagnóstico
- `backend/testar_geracao_orcamento.py` - Script de teste
- `backend/criar_template_exemplo.py` - Cria template pronto
- `docs/SOLUCAO_ERRO_PDF.md` - Documentação detalhada
- `SOLUCAO_RAPIDA_PDF.md` - Guia rápido

## ✨ Resultado Esperado

Após seguir os passos, ao clicar em "Gerar PDF":
1. ✅ Requisição retorna status 200
2. ✅ Arquivo .docx é baixado automaticamente
3. ✅ Arquivo contém todos os dados do orçamento
4. ✅ Variáveis foram substituídas corretamente
5. ✅ Formatação preservada
