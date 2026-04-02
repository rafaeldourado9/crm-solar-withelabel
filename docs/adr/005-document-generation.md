# ADR-005: Geracao de Documentos sem LibreOffice

## Status
Aceita

## Contexto
Geracao atual de PDF usa subprocess do LibreOffice com timeout de 30s.
Fragil, lento, depende de pacote de sistema, cria temp files sem cleanup.

## Decisao
Usar python-docx para DOCX + WeasyPrint para PDF.

## Implementacao

1. **DOCX**: python-docx com engine de substituicao robusta
   - Busca em paragrafos E runs (resolve problema de variaveis fragmentadas)
   - Busca em tabelas recursivamente
   - Validacao: lista variaveis esperadas vs encontradas

2. **PDF**: WeasyPrint (HTML -> PDF)
   - Renderiza HTML/CSS para PDF nativo
   - Sem dependencia de LibreOffice
   - Suporta CSS para layout profissional

3. **Templates**: Upload por tenant no modulo `documentos/`
   - Cada tenant pode ter seus proprios templates
   - Validacao de variaveis no upload

## Consequencias

### Positivas
- Sem subprocess, sem temp files
- 10x mais rapido que LibreOffice
- Funciona em qualquer container Python
- Templates customizaveis por tenant

### Negativas
- WeasyPrint precisa de cairo/pango (libs de sistema, mas leves)
- Layout PDF via HTML/CSS (nao WYSIWYG como LibreOffice)
