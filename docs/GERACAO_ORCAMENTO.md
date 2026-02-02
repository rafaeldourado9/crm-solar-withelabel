# Geração de Orçamento com Template

## 🎯 Funcionalidade

Sistema de geração automática de orçamentos em formato DOCX usando templates personalizados.

## 📋 Como Usar

### 1. Cadastrar Template

1. Acesse **Templates** no menu
2. Clique em **Novo Template**
3. Preencha:
   - Nome: "Orçamento Padrão"
   - Tipo: **Orçamento**
   - Arquivo: Selecione seu template .docx
4. Clique em **Salvar**

### 2. Preparar Template DOCX

No seu arquivo Word, use as variáveis no formato `{{NOME_VARIAVEL}}`:

```
ORÇAMENTO Nº {{NUMERO_ORCAMENTO}}

Cliente: {{NOME_CLIENTE}}
CPF/CNPJ: {{CPF_CNPJ}}

Sistema: {{POTENCIA_KWP}} kWp
Painéis: {{QUANTIDADE_PAINEIS}}x {{MARCA_PAINEL}} {{POTENCIA_PAINEL}}W
Inversor: {{MARCA_INVERSOR}} {{POTENCIA_INVERSOR_KW}} kW

VALOR FINAL: {{VALOR_FINAL}}
```

📖 **Lista completa de variáveis:** [VARIAVEIS_TEMPLATE_ORCAMENTO.md](./VARIAVEIS_TEMPLATE_ORCAMENTO.md)

### 3. Gerar Orçamento

1. Acesse **Orçamentos**
2. Clique em um orçamento para ver detalhes
3. Clique no botão **Gerar PDF**
4. O arquivo será baixado automaticamente

## ✨ Recursos

- ✅ Substituição automática de variáveis
- ✅ Formatação preservada (negrito, cores, tabelas)
- ✅ Valores monetários formatados (R$ 1.000,00)
- ✅ Datas no formato brasileiro (DD/MM/YYYY)
- ✅ Cálculos automáticos (geração, potência, etc)
- ✅ Download direto do navegador

## 🔧 Teste

Execute o script de teste:

```bash
cd backend
python testar_geracao_orcamento.py
```

Isso irá:
1. Verificar se existe template ativo
2. Buscar um orçamento
3. Gerar arquivo de teste
4. Salvar como `teste_orcamento_XXX.docx`

## 📝 Variáveis Principais

| Variável | Descrição | Exemplo |
|----------|-----------|---------|
| `{{NOME_CLIENTE}}` | Nome do cliente | João Silva |
| `{{NUMERO_ORCAMENTO}}` | Número do orçamento | ORC-0001 |
| `{{POTENCIA_KWP}}` | Potência do sistema | 5.40 |
| `{{QUANTIDADE_PAINEIS}}` | Qtd de painéis | 12 |
| `{{VALOR_FINAL}}` | Valor final | R$ 25.000,00 |
| `{{FORMA_PAGAMENTO}}` | Pagamento | À vista ou 12x de R$ 2.500,00 |

## 🚨 Troubleshooting

### Erro: "Nenhum template de orçamento ativo encontrado"
- Cadastre um template do tipo "Orçamento"
- Certifique-se que está marcado como "Ativo"

### Variáveis não são substituídas
- Verifique se está usando `{{VARIAVEL}}` (maiúsculas, duas chaves)
- Confira a lista de variáveis disponíveis na documentação

### Arquivo não baixa
- Verifique o console do navegador (F12)
- Confirme que o backend está rodando
- Teste com o script `testar_geracao_orcamento.py`

## 📚 Documentação Relacionada

- [Variáveis de Template](./VARIAVEIS_TEMPLATE_ORCAMENTO.md)
- [Sistema de Templates](./SISTEMA_AUTOMATICO_TEMPLATES.md)
- [API de Orçamentos](./API.md#orçamentos)
