# Sprint 03 - Documentos (Propostas + Contratos + DOCX/PDF)

**Objetivo**: Fluxo comercial completo com geracao de documentos.

**Depende de**: Sprint 02 completa.

---

## Tasks

### 3.1 Modulo Documentos (Engine de Templates)
- [x] Domain: TemplateEngine service
  - Substituicao robusta de variaveis em DOCX (paragrafos + runs + tabelas)
  - Validacao: variaveis esperadas vs encontradas no template
  - Suporte a formatacao brasileira (moeda, datas, extenso)
- [x] Domain: numero_por_extenso() - converter valores para portugues
- [x] Infrastructure: adapter python-docx (gerar_docx, extrair_variaveis_docx)
- [x] Infrastructure: adapter WeasyPrint (HTML -> PDF, sem LibreOffice)
- [x] Testes: TemplateEngine + numero_por_extenso cobertos em test_domain.py

**Criterio**: Template com variaveis gera DOCX correto. PDF gerado sem LibreOffice.

### 3.2 Modulo Propostas
- [x] Domain: entidade Proposta (status: pendente/aceita/recusada)
- [x] Domain: state machine (aceitar/recusar com validacoes)
- [x] Domain: conversao automatica Orcamento -> Proposta (snapshot cliente)
- [x] Infrastructure: model + migration (007_create_propostas_table.py)
- [x] Application: CriarProposta, ListarPropostas, ObterProposta, Aceitar, Recusar
- [x] API: POST /propostas, GET /propostas, POST /propostas/{id}/aceitar, /recusar
- [x] Testes unitarios de dominio

**Criterio**: Converter orcamento cria proposta. Aceitar proposta muda status.

### 3.3 Modulo Contratos
- [x] Domain: entidade Contrato (dados empresa do TENANT, nao hardcoded)
- [x] Domain: state machine (rascunho -> assinado -> em_execucao -> concluido)
- [x] Domain: conversao Proposta -> Contrato (puxa dados do Tenant automaticamente)
- [x] Infrastructure: model + migration (008_create_contratos_table.py)
- [x] Application: CriarContrato, ListarContratos, ObterContrato, AtualizarContrato
- [x] API: CRUD + GET /contratos/{id}/gerar-pdf
- [x] Variaveis do template preenchidas pelo tenant (empresa, banco, etc.)
- [x] Testes unitarios de dominio

**Criterio**: Contrato gerado com dados da empresa do tenant. PDF baixa.

### 3.4 Modulo Templates (Upload)
- [x] Domain: entidade Template (nome, tipo, arquivo, ativo)
- [x] Infrastructure: model + storage local + migration (009_create_templates_table.py)
- [x] Application: Upload (extrai variaveis automaticamente), Listar, Deletar
- [x] API: POST /templates (upload multipart), GET /templates, DELETE /templates/{id}
- [x] Validacao: so aceita .docx, tipo valido obrigatorio
- [x] Auto-desativa template anterior do mesmo tipo ao fazer upload

**Criterio**: Upload de template DOCX funciona. Template invalido e rejeitado.

### 3.5 Integracao Frontend - Documentos
- [x] api.js: propostasAPI, contratosAPI, templatesAPI adicionados
- [x] Download de PDF via API (responseType blob)
- [x] Propostas.jsx: response paginado, aceitar/recusar com ConfirmDialog, botao Gerar Contrato
- [x] Contratos.jsx: filtro por status, botao Avancar status, PDF download, dados do tenant
- [x] Templates.jsx: upload via templatesAPI, download, preview docx-preview, chaves atualizadas

**Criterio**: Fluxo completo: orcamento -> proposta -> contrato -> download PDF.

---

## Entregavel
- [x] Propostas criadas a partir de orcamentos (com snapshot do cliente)
- [x] Contratos com dados do tenant (WhiteLabel — zero hardcode)
- [x] DOCX gerado com substituicao robusta (handles split runs)
- [x] PDF gerado via WeasyPrint (sem LibreOffice)
- [x] Templates customizaveis por upload (ativo por tipo)
- [x] Migrations 007, 008, 009 criadas
- [x] weasyprint adicionado ao pyproject.toml
- [x] 4 novos routers registrados no main.py
