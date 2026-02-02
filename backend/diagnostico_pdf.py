#!/usr/bin/env python
"""
Script de diagnóstico para geração de PDF
"""
import os
import sys
import django

# Configurar Django
sys.path.insert(0, os.path.dirname(__file__))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.templates.models import Template
from apps.orcamentos.models import Orcamento

def diagnosticar():
    print("=" * 60)
    print("DIAGNÓSTICO - GERAÇÃO DE PDF")
    print("=" * 60)
    
    # 1. Verificar biblioteca python-docx
    print("\n1. Verificando biblioteca python-docx...")
    try:
        import docx
        print("   ✓ python-docx instalado")
    except ImportError:
        print("   ✗ python-docx NÃO instalado")
        print("   → Execute: pip install python-docx")
        return False
    
    # 2. Verificar templates cadastrados
    print("\n2. Verificando templates cadastrados...")
    templates = Template.objects.filter(tipo='orcamento', ativo=True)
    
    if templates.exists():
        print(f"   ✓ {templates.count()} template(s) de orçamento ativo(s)")
        for t in templates:
            print(f"     - {t.nome} (arquivo: {t.arquivo.name})")
            # Verificar se arquivo existe
            if os.path.exists(t.arquivo.path):
                print(f"       ✓ Arquivo existe: {t.arquivo.path}")
            else:
                print(f"       ✗ Arquivo NÃO existe: {t.arquivo.path}")
    else:
        print("   ✗ Nenhum template de orçamento ativo encontrado")
        print("   → Cadastre um template em: http://localhost:8000/admin/templates/template/")
        return False
    
    # 3. Verificar orçamentos
    print("\n3. Verificando orçamentos...")
    orcamentos = Orcamento.objects.all()[:5]
    
    if orcamentos.exists():
        print(f"   ✓ {Orcamento.objects.count()} orçamento(s) cadastrado(s)")
        print("   Últimos 5:")
        for orc in orcamentos:
            print(f"     - ID: {orc.id} | {orc.numero} | {orc.cliente_nome}")
    else:
        print("   ✗ Nenhum orçamento cadastrado")
        return False
    
    # 4. Testar geração
    print("\n4. Testando geração de PDF...")
    try:
        orcamento = orcamentos.first()
        template = templates.first()
        
        from apps.orcamentos.services.template_processor import TemplateProcessorService
        from apps.premissas.models import Premissa
        
        premissa = Premissa.get_ativa()
        cliente = orcamento.cliente
        
        print(f"   Processando orçamento {orcamento.numero}...")
        buffer = TemplateProcessorService.processar_template(
            template.arquivo.path,
            orcamento,
            premissa,
            cliente
        )
        
        # Salvar arquivo de teste
        output_path = f"teste_orcamento_{orcamento.id}.docx"
        with open(output_path, 'wb') as f:
            f.write(buffer.getvalue())
        
        print(f"   ✓ PDF gerado com sucesso!")
        print(f"   → Arquivo salvo em: {os.path.abspath(output_path)}")
        
    except Exception as e:
        print(f"   ✗ Erro ao gerar PDF: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    # 5. Verificar endpoint
    print("\n5. Verificando endpoint...")
    print(f"   URL correta: http://localhost:8000/api/orcamentos/{orcamento.id}/gerar-pdf-dimensionamento/")
    print(f"   Método: GET")
    print(f"   Headers: Authorization: Token <seu_token>")
    
    print("\n" + "=" * 60)
    print("DIAGNÓSTICO CONCLUÍDO COM SUCESSO!")
    print("=" * 60)
    return True

if __name__ == '__main__':
    diagnosticar()
