# Como Adicionar Gráficos Dinâmicos nos Templates

## Opção 1: Gráficos Gerados Automaticamente (Recomendado)

O sistema gera gráficos como imagens e insere automaticamente no documento.

### Chaves Disponíveis para Gráficos:

```
{{GRAFICO_GERACAO_ANUAL}}       - Gráfico de geração ao longo de 25 anos
{{GRAFICO_ECONOMIA_MENSAL}}     - Gráfico de economia mensal
{{GRAFICO_PAYBACK}}             - Gráfico de retorno do investimento
```

### Como Usar no Word:

1. No seu documento Word, insira a chave onde quer o gráfico:
   ```
   {{GRAFICO_GERACAO_ANUAL}}
   ```

2. O sistema substituirá pela imagem do gráfico gerado

### Tipos de Gráficos:

#### 1. Geração Anual (25 anos)
- Mostra a geração estimada considerando perda de eficiência
- Linha com área preenchida
- Eixo X: Anos (1-25)
- Eixo Y: Geração (kWh/ano)

#### 2. Economia Mensal
- Barras mostrando economia mês a mês
- Considera variação sazonal
- Valores em R$ acima de cada barra

#### 3. Payback
- Linha vermelha: Investimento inicial
- Linha verde: Economia acumulada
- Marca o ponto de payback (quando economia = investimento)

---

## Opção 2: Usar Gráficos do Excel/Word

Se preferir manter gráficos editáveis no Word:

1. Crie um gráfico no Word com dados de exemplo
2. Use chaves para os valores:
   ```
   Série 1: {{GERACAO_ANO_1}}, {{GERACAO_ANO_2}}, ...
   ```
3. O sistema atualizará os valores, mas você precisará atualizar o gráfico manualmente

---

## Opção 3: Gráficos Externos (Mais Simples)

1. Deixe um espaço no documento com texto:
   ```
   [GRÁFICO SERÁ INSERIDO AQUI]
   ```

2. Após gerar o PDF, adicione o gráfico manualmente usando ferramentas de edição de PDF

---

## Implementação Técnica

### Backend (Python):
```python
from apps.orcamentos.services.grafico_service import GraficoService

# Gerar gráfico
grafico_base64 = GraficoService.gerar_grafico_geracao_anual(orcamento, premissa)

# Substituir no template
template = template.replace('{{GRAFICO_GERACAO_ANUAL}}', f'<img src="{grafico_base64}" />')
```

### Bibliotecas Necessárias:
```bash
pip install matplotlib
pip install python-docx
pip install docx2pdf
```

---

## Exemplo Completo no Template Word:

```
ANÁLISE DE GERAÇÃO

O sistema instalado terá capacidade de {{POTENCIA_TOTAL_KWP}} kWp e 
gerará aproximadamente {{GERACAO_ESTIMADA_KWH}} kWh/mês.

{{GRAFICO_GERACAO_ANUAL}}

ECONOMIA ESTIMADA

Com base na tarifa atual de R$ {{TARIFA_ENERGIA}}/kWh, a economia 
mensal será de aproximadamente R$ {{ECONOMIA_MENSAL}}.

{{GRAFICO_ECONOMIA_MENSAL}}

RETORNO DO INVESTIMENTO

O investimento de R$ {{VALOR_FINAL}} terá retorno estimado em 
{{PAYBACK_ANOS}} anos.

{{GRAFICO_PAYBACK}}
```

---

## Próximos Passos:

1. Instale as dependências no backend
2. Adicione as chaves de gráfico no seu template Word
3. O sistema gerará os gráficos automaticamente ao criar PDF
4. Personalize cores e estilos no arquivo `grafico_service.py`
