from docx import Document
from docx.shared import Inches
import re
from decimal import Decimal
from io import BytesIO

class TemplateProcessorService:
    """
    Processa templates Word/DOCX e substitui chaves pelos valores reais
    """
    
    @staticmethod
    def processar_template(template_path, orcamento, premissa, cliente):
        """
        Processa um template DOCX e substitui todas as chaves
        """
        doc = Document(template_path)
        
        # Montar dicionário de substituições
        substituicoes = TemplateProcessorService._montar_substituicoes(orcamento, premissa, cliente)
        
        # Substituir em parágrafos
        for paragrafo in doc.paragraphs:
            TemplateProcessorService._substituir_texto(paragrafo, substituicoes)
        
        # Substituir em tabelas
        for tabela in doc.tables:
            for linha in tabela.rows:
                for celula in linha.cells:
                    for paragrafo in celula.paragraphs:
                        TemplateProcessorService._substituir_texto(paragrafo, substituicoes)
        
        # Salvar em buffer
        buffer = BytesIO()
        doc.save(buffer)
        buffer.seek(0)
        return buffer
    
    @staticmethod
    def _montar_substituicoes(orcamento, premissa, cliente):
        """
        Monta dicionário com todas as chaves e valores
        """
        potencia_total_kwp = (orcamento.quantidade_paineis * orcamento.potencia_painel) / 1000
        geracao_mensal = potencia_total_kwp * float(premissa.hsp_padrao) * 30 * (1 - float(premissa.perda_padrao))
        geracao_anual = geracao_mensal * 12
        
        # Calcular payback
        economia_mensal = geracao_mensal * float(premissa.tarifa_energia_atual)
        payback_meses = float(orcamento.valor_final) / economia_mensal if economia_mensal > 0 else 0
        payback_anos = payback_meses / 12
        
        return {
            # Orçamento
            '{{NUMERO_ORCAMENTO}}': orcamento.numero,
            '{{DATA_CRIACAO}}': orcamento.data_criacao.strftime('%d/%m/%Y'),
            '{{NOME_KIT}}': orcamento.nome_kit,
            '{{VALIDADE_PROPOSTA_DIAS}}': str(orcamento.validade_dias),
            
            # Cliente
            '{{CLIENTE_NOME}}': cliente.nome,
            '{{CLIENTE_CPF_CNPJ}}': cliente.cpf_cnpj or '',
            '{{CLIENTE_TELEFONE}}': cliente.telefone or '',
            '{{CLIENTE_EMAIL}}': cliente.email or '',
            '{{CLIENTE_ENDERECO}}': cliente.endereco or '',
            '{{CLIENTE_BAIRRO}}': cliente.bairro or '',
            '{{CLIENTE_CIDADE}}': cliente.cidade,
            '{{CLIENTE_ESTADO}}': cliente.estado,
            '{{CLIENTE_CEP}}': cliente.cep or '',
            
            # Painéis
            '{{PAINEIS_QTD}}': str(orcamento.quantidade_paineis),
            '{{PAINEIS_MARCA}}': orcamento.marca_painel,
            '{{PAINEIS_POTENCIA}}': str(orcamento.potencia_painel),
            '{{PAINEIS_POTENCIA_TOTAL}}': str(orcamento.quantidade_paineis * orcamento.potencia_painel),
            
            # Inversor
            '{{INVERSOR_QTD}}': str(orcamento.quantidade_inversores),
            '{{INVERSOR_MARCA}}': orcamento.marca_inversor,
            '{{INVERSOR_POTENCIA}}': str(orcamento.potencia_inversor),
            
            # Técnico
            '{{POTENCIA_TOTAL_KWP}}': f'{potencia_total_kwp:.2f}',
            '{{GERACAO_ESTIMADA_KWH}}': f'{geracao_mensal:.0f}',
            '{{GERACAO_ANUAL_KWH}}': f'{geracao_anual:.0f}',
            '{{HSP}}': str(premissa.hsp_padrao),
            '{{PERDA_SISTEMA}}': f'{float(premissa.perda_padrao) * 100:.1f}',
            '{{TIPO_ESTRUTURA}}': orcamento.get_tipo_estrutura_display(),
            
            # Valores
            '{{VALOR_KIT}}': f'{float(orcamento.valor_kit):,.2f}',
            '{{VALOR_PROJETO}}': f'{float(premissa.valor_projeto):,.2f}',
            '{{VALOR_MONTAGEM}}': f'{float(premissa.montagem_por_painel * orcamento.quantidade_paineis):,.2f}',
            '{{VALOR_ESTRUTURA}}': f'{float(orcamento.valor_estrutura):,.2f}',
            '{{VALOR_MATERIAL_ELETRICO}}': f'{float(orcamento.valor_material_eletrico):,.2f}',
            '{{CUSTO_TOTAL}}': f'{float(orcamento.valor_total):,.2f}',
            '{{VALOR_FINAL}}': f'{float(orcamento.valor_final):,.2f}',
            
            # Financeiro
            '{{FORMA_PAGAMENTO}}': orcamento.forma_pagamento,
            '{{NUMERO_PARCELAS}}': orcamento.forma_pagamento if orcamento.forma_pagamento != 'avista' else '1',
            '{{VALOR_PARCELA}}': f'{float(orcamento.valor_parcela):,.2f}' if orcamento.valor_parcela else f'{float(orcamento.valor_final):,.2f}',
            '{{TAXA_JUROS}}': str(orcamento.taxa_juros),
            
            # Margens
            '{{COMISSAO_PERCENTUAL}}': str(orcamento.comissao_percentual or premissa.comissao_percentual),
            '{{IMPOSTO_PERCENTUAL}}': str(orcamento.imposto_percentual or premissa.imposto_percentual),
            '{{LUCRO_PERCENTUAL}}': str(orcamento.margem_lucro_percentual or premissa.margem_lucro_percentual),
            
            # Prazos
            '{{PRAZO_ENTREGA}}': str(premissa.prazo_entrega_padrao),
            '{{GARANTIA_INSTALACAO}}': str(premissa.garantia_instalacao_meses),
            
            # Análise
            '{{ECONOMIA_MENSAL}}': f'{economia_mensal:,.2f}',
            '{{PAYBACK_ANOS}}': f'{payback_anos:.1f}',
            '{{TARIFA_ENERGIA}}': f'{float(premissa.tarifa_energia_atual):.4f}',
            
            # Vendedor (se houver)
            '{{VENDEDOR_NOME}}': orcamento.vendedor.nome if orcamento.vendedor else '',
            '{{VENDEDOR_TELEFONE}}': orcamento.vendedor.telefone if orcamento.vendedor else '',
            '{{VENDEDOR_EMAIL}}': orcamento.vendedor.email if orcamento.vendedor else '',
        }
    
    @staticmethod
    def _substituir_texto(paragrafo, substituicoes):
        """
        Substitui chaves no texto mantendo formatação
        Suporta {{CHAVE}} e [chave]
        """
        texto_completo = ''.join([run.text for run in paragrafo.runs])
        
        # Verificar se há chaves no texto
        if ('{{' in texto_completo and '}}' in texto_completo) or ('[' in texto_completo and ']' in texto_completo):
            # Substituir todas as chaves {{}}
            for chave, valor in substituicoes.items():
                texto_completo = texto_completo.replace(chave, valor)
            
            # Substituir chaves [] convertendo para maiúsculas
            import re
            def substituir_colchetes(match):
                chave_original = match.group(1)
                chave_upper = '{{' + chave_original.upper().replace(' ', '_') + '}}'
                return substituicoes.get(chave_upper, match.group(0))
            
            texto_completo = re.sub(r'\[([^\]]+)\]', substituir_colchetes, texto_completo)
            
            # Limpar runs e adicionar texto substituído
            for run in paragrafo.runs:
                run.text = ''
            if paragrafo.runs:
                paragrafo.runs[0].text = texto_completo
            else:
                paragrafo.add_run(texto_completo)
