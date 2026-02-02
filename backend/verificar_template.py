#!/usr/bin/env python
import os
import sys
import django

sys.path.insert(0, os.path.dirname(__file__))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.templates.models import Template
from docx import Document

t = Template.objects.filter(tipo='orcamento', ativo=True).first()
print(f'Template: {t.nome}')
print(f'Arquivo: {t.arquivo.path}')

doc = Document(t.arquivo.path)
print('\nTexto do template:')
print('=' * 60)
for p in doc.paragraphs[:50]:
    if p.text.strip():
        print(p.text)
