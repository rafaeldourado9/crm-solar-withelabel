from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from io import BytesIO
from datetime import datetime, timedelta

class PDFOrcamentoService:
    
    @staticmethod
    def gerar_pdf_orcamento(orcamento):
        """Gera PDF do orçamento"""
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4, topMargin=2*cm, bottomMargin=2*cm)
        elements = []
        styles = getSampleStyleSheet()
        
        # Título
        title_style = ParagraphStyle('CustomTitle', parent=styles['Heading1'], alignment=TA_CENTER, fontSize=16, textColor=colors.HexColor('#1a5490'))
        elements.append(Paragraph(f"PROPOSTA: {orcamento.numero}", title_style))
        elements.append(Spacer(1, 0.5*cm))
        
        # Informações do Cliente
        elements.append(Paragraph("<b>INFORMAÇÕES DO CLIENTE</b>", styles['Heading2']))
        cliente_data = [
            ['Nome/Razão Social:', orcamento.cliente.nome],
            ['Cidade:', orcamento.cliente.cidade],
            ['Telefone:', orcamento.cliente.telefone or 'N/A'],
        ]
        cliente_table = Table(cliente_data, colWidths=[5*cm, 10*cm])
        cliente_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ]))
        elements.append(cliente_table)
        elements.append(Spacer(1, 0.5*cm))
        
        # Dados Adicionais
        elements.append(Paragraph("<b>DADOS ADICIONAIS</b>", styles['Heading2']))
        validade = orcamento.data_criacao + timedelta(days=orcamento.validade_dias)
        dados_data = [
            ['Consumo Médio:', f"{orcamento.consumo_medio_kwh} kWh"],
            ['Economia mensal esperada:', f"R$ {orcamento.economia_mensal}"],
            ['Economia Esperada (%):', f"{orcamento.economia_percentual}%"],
            ['Data de Criação:', orcamento.data_criacao.strftime('%d/%m/%Y')],
            ['Validade da Proposta:', f"{orcamento.validade_dias} dias"],
        ]
        dados_table = Table(dados_data, colWidths=[6*cm, 9*cm])
        dados_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ]))
        elements.append(dados_table)
        elements.append(Spacer(1, 0.5*cm))
        
        # Dimensionamento
        elements.append(Paragraph("<b>DIMENSIONAMENTO - SISTEMA GERADOR ON GRID</b>", styles['Heading2']))
        dim_data = [
            ['Geração de Energia Requerida:', f"{orcamento.geracao_requerida_kwh} kWh"],
            ['Potência Instalada:', f"{orcamento.potencia_instalada_kwp} kWp"],
            ['Potência das placas:', f"{orcamento.potencia_placas_w} W"],
            ['Quantidade de placas:', str(orcamento.quantidade_placas)],
            ['Área necessária:', f"{orcamento.area_necessaria_m2} m²"],
        ]
        dim_table = Table(dim_data, colWidths=[6*cm, 9*cm])
        dim_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ]))
        elements.append(dim_table)
        elements.append(Spacer(1, 0.5*cm))
        
        # Equipamentos
        elements.append(Paragraph("<b>EQUIPAMENTO</b>", styles['Heading2']))
        equip_data = [
            ['ITEM', 'QUANTIDADE'],
            [orcamento.modelo_placa, str(orcamento.quantidade_placas)],
            [orcamento.modelo_inversor, str(orcamento.quantidade_inversores)],
            ['PROJETO & INSTALAÇÃO', 'Incluso'],
        ]
        equip_table = Table(equip_data, colWidths=[10*cm, 5*cm])
        equip_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1a5490')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ]))
        elements.append(equip_table)
        elements.append(Spacer(1, 0.5*cm))
        
        # Valor Total
        valor_style = ParagraphStyle('Valor', parent=styles['Normal'], fontSize=14, textColor=colors.HexColor('#1a5490'), alignment=TA_CENTER)
        elements.append(Paragraph(f"<b>Valor Total: R$ {orcamento.valor_total}</b>", valor_style))
        
        doc.build(elements)
        buffer.seek(0)
        return buffer
