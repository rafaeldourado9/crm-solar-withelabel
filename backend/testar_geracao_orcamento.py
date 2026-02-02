#!/usr/bin/env python
"""
Script de teste para geração de orçamento
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
from apps.premissas.models import Premissa

def testar():
    print("Testando geração de orçamento...")
    
    # Buscar template
    template = Template.objects.filter(tipo='orcamento', ativo=True).first()
    
    if not template:
        print("❌ ERRO: Nenhum template de orçamento ativo encontrado!")
        print("\nSolução:")
        print("1. Acesse: http://localhost:8000/admin/templates/template/")
        print("2. Cadastre um template do tipo 'Orçamento'")
        print("3. Marque como 'Ativo'")
        return
    
    print(f"✓ Template encontrado: {template.nome}")
    
    # Buscar orçamento
    orcamento = Orcamento.objects.first()
    
    if not orcamento:
        print("❌ ERRO: Nenhum orçamento cadastrado!")
        return
    
    print(f"✓ Orçamento encontrado: {orcamento.numero}")
    
    # Buscar premissa
    premissa = Premissa.get_ativa()
    print(f"✓ Premissa ativa encontrada")
    
    # Buscar cliente
    cliente = orcamento.cliente
    print(f"✓ Cliente: {cliente.nome}")
    
    # Processar template
    try:
        from apps.orcamentos.services.template_processor import TemplateProcessorService
        
        print("\nProcessando template...")
        buffer = TemplateProcessorService.processar_template(
            template.arquivo.path,
            orcamento,
            premissa,
            cliente
        )
        
        # Salvar arquivo
        output_path = f"teste_orcamento_{orcamento.id}.docx"
        with open(output_path, 'wb') as f:
            f.write(buffer.getvalue())
        
        print(f"\n✅ SUCESSO! Arquivo gerado: {os.path.abspath(output_path)}")
        print(f"\nTamanho: {len(buffer.getvalue())} bytes")
        
    except Exception as e:
        print(f"\n❌ ERRO ao processar template:")
        print(f"   {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    testar()
