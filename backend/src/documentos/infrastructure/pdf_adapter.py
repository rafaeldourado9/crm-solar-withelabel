"""Adapter WeasyPrint: converte HTML estilizado para PDF."""
from src.documentos.domain.services import TemplateEngine

_HTML_BASE = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<style>
  body {{ font-family: Arial, sans-serif; font-size: 11pt; color: #222; margin: 2cm; }}
  h1 {{ color: #1a56db; font-size: 16pt; border-bottom: 2px solid #1a56db; padding-bottom: 6px; }}
  h2 {{ font-size: 12pt; color: #374151; margin-top: 18px; }}
  table {{ width: 100%; border-collapse: collapse; margin-top: 10px; }}
  th {{ background: #1a56db; color: white; padding: 6px 8px; text-align: left; }}
  td {{ padding: 5px 8px; border-bottom: 1px solid #e5e7eb; }}
  .valor {{ font-size: 14pt; font-weight: bold; color: #1a56db; }}
  .footer {{ margin-top: 30px; font-size: 9pt; color: #6b7280; text-align: center; }}
  .section {{ margin-top: 20px; }}
</style>
</head>
<body>
{conteudo}
</body>
</html>"""


def _html_orcamento(v: dict[str, str]) -> str:
    return f"""
<h1>Orçamento Solar #{v.get('NUMERO_ORCAMENTO', '')}</h1>
<p><strong>Data:</strong> {v.get('DATA_ORCAMENTO', '')} &nbsp;|&nbsp;
   <strong>Validade:</strong> {v.get('DATA_VALIDADE', '')}</p>

<div class="section">
<h2>Cliente</h2>
<table>
  <tr><td><strong>Nome</strong></td><td>{v.get('CLIENTE_NOME', '')}</td></tr>
  <tr><td><strong>CPF/CNPJ</strong></td><td>{v.get('CLIENTE_CPF_CNPJ', '')}</td></tr>
  <tr><td><strong>Endereço</strong></td><td>{v.get('CLIENTE_ENDERECO', '')}, {v.get('CLIENTE_CIDADE', '')}/{v.get('CLIENTE_ESTADO', '')}</td></tr>
  <tr><td><strong>Telefone</strong></td><td>{v.get('CLIENTE_TELEFONE', '')}</td></tr>
  <tr><td><strong>Email</strong></td><td>{v.get('CLIENTE_EMAIL', '')}</td></tr>
</table>
</div>

<div class="section">
<h2>Dimensionamento Técnico</h2>
<table>
  <tr><td><strong>Potência do Sistema</strong></td><td>{v.get('POTENCIA_KWP', '')} kWp</td></tr>
  <tr><td><strong>Painéis</strong></td><td>{v.get('QUANTIDADE_PAINEIS', '')} x {v.get('MODELO_PAINEL', '')} ({v.get('POTENCIA_PAINEL_W', '')} W)</td></tr>
  <tr><td><strong>Inversor</strong></td><td>{v.get('MODELO_INVERSOR', '')} ({v.get('POTENCIA_INVERSOR_W', '')} W)</td></tr>
  <tr><td><strong>Geração Estimada</strong></td><td>{v.get('GERACAO_MENSAL_KWH', '')} kWh/mês</td></tr>
</table>
</div>

<div class="section">
<h2>Investimento</h2>
<table>
  <tr><th>Item</th><th>Valor</th></tr>
  <tr><td>Kit Solar (Painéis + Inversor)</td><td>R$ {v.get('VALOR_KIT', '')}</td></tr>
  <tr><td>Estrutura de Fixação</td><td>R$ {v.get('VALOR_ESTRUTURA', '')}</td></tr>
  <tr><td>Material Elétrico</td><td>R$ {v.get('VALOR_MATERIAL_ELETRICO', '')}</td></tr>
  <tr><td>Mão de Obra (Montagem)</td><td>R$ {v.get('VALOR_MONTAGEM', '')}</td></tr>
  <tr><td>Projeto Elétrico</td><td>R$ {v.get('VALOR_PROJETO', '')}</td></tr>
  <tr><td>Deslocamento</td><td>R$ {v.get('CUSTO_DESLOCAMENTO', '')}</td></tr>
</table>
<p class="valor">Valor Total: R$ {v.get('VALOR_FINAL', '')}</p>
<p><strong>Pagamento:</strong> {v.get('FORMA_PAGAMENTO', '')}
   {' — ' + v.get('NUMERO_PARCELAS', '') + 'x de R$ ' + v.get('VALOR_PARCELA', '') if v.get('NUMERO_PARCELAS', '0') != '0' else ''}
</p>
</div>

<div class="footer">Proposta válida até {v.get('DATA_VALIDADE', '')} • Gerado por SunOps</div>
"""


def _html_contrato(v: dict[str, str]) -> str:
    return f"""
<h1>Contrato de Fornecimento e Instalação de Sistema Solar</h1>

<div class="section">
<h2>Partes</h2>
<table>
  <tr><th colspan="2">Contratada (Empresa)</th></tr>
  <tr><td><strong>Razão Social</strong></td><td>{v.get('empresa_razao_social', '')}</td></tr>
  <tr><td><strong>CNPJ</strong></td><td>{v.get('empresa_cnpj', '')}</td></tr>
  <tr><td><strong>Endereço</strong></td><td>{v.get('empresa_endereco', '')}, {v.get('empresa_cidade', '')}</td></tr>
  <tr><td><strong>Representante</strong></td><td>{v.get('empresa_representante_nome', '')} — CPF: {v.get('empresa_representante_cpf', '')}</td></tr>
  <tr><th colspan="2">Contratante (Cliente)</th></tr>
  <tr><td><strong>Nome</strong></td><td>{v.get('cliente_nome', '')}</td></tr>
  <tr><td><strong>CPF/CNPJ</strong></td><td>{v.get('cliente_cpf_cnpj', '')}</td></tr>
  <tr><td><strong>Endereço</strong></td><td>{v.get('cliente_endereco', '')}, {v.get('cliente_bairro', '')}, {v.get('cliente_cidade', '')}/{v.get('cliente_estado', '')} — CEP {v.get('cliente_cep', '')}</td></tr>
</table>
</div>

<div class="section">
<h2>Objeto do Contrato</h2>
<table>
  <tr><td><strong>Sistema</strong></td><td>{v.get('potencia_total', '')} kWp — {v.get('quantidade_paineis', '')} painéis</td></tr>
  <tr><td><strong>Valor Total</strong></td><td class="valor">R$ {v.get('valor_total', '')} ({v.get('valor_total_extenso', '')})</td></tr>
  <tr><td><strong>Parcelas</strong></td><td>{v.get('numero_parcelas', '')}x de R$ {v.get('valor_parcela', '')} ({v.get('valor_parcela_extenso', '')})</td></tr>
</table>
</div>

<div class="section">
<h2>Dados Bancários para Pagamento</h2>
<table>
  <tr><td><strong>Banco</strong></td><td>{v.get('banco_nome', '')}</td></tr>
  <tr><td><strong>Agência</strong></td><td>{v.get('banco_agencia', '')}</td></tr>
  <tr><td><strong>Conta</strong></td><td>{v.get('banco_conta', '')}</td></tr>
  <tr><td><strong>Titular</strong></td><td>{v.get('banco_titular', '')}</td></tr>
</table>
</div>

<div class="section">
<h2>Termos</h2>
<table>
  <tr><td><strong>Prazo de Execução</strong></td><td>{v.get('prazo_execucao_dias', '')} dias úteis</td></tr>
  <tr><td><strong>Garantia da Instalação</strong></td><td>{v.get('garantia_instalacao_meses', '')} meses</td></tr>
  <tr><td><strong>Foro</strong></td><td>Comarca de {v.get('foro_comarca', '')}</td></tr>
</table>
</div>

<div class="footer">Contrato gerado por SunOps • {v.get('empresa_razao_social', '')}</div>
"""


def gerar_pdf_orcamento(variaveis: dict[str, str]) -> bytes:
    """Gera PDF de orçamento usando WeasyPrint."""
    try:
        from weasyprint import HTML  # type: ignore[import]
        conteudo = _html_orcamento(variaveis)
        html = _HTML_BASE.format(conteudo=conteudo)
        return HTML(string=html).write_pdf()  # type: ignore[no-any-return]
    except ImportError as e:
        raise RuntimeError(
            "WeasyPrint não instalado. Instale com: pip install weasyprint"
        ) from e


def gerar_pdf_contrato(variaveis: dict[str, str]) -> bytes:
    """Gera PDF de contrato usando WeasyPrint."""
    try:
        from weasyprint import HTML  # type: ignore[import]
        conteudo = _html_contrato(variaveis)
        html = _HTML_BASE.format(conteudo=conteudo)
        return HTML(string=html).write_pdf()  # type: ignore[no-any-return]
    except ImportError as e:
        raise RuntimeError(
            "WeasyPrint não instalado. Instale com: pip install weasyprint"
        ) from e
