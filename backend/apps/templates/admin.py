from django.contrib import admin
from .models import Template

@admin.register(Template)
class TemplateAdmin(admin.ModelAdmin):
    list_display = ['nome', 'tipo', 'ativo', 'created_at']
    list_filter = ['tipo', 'ativo']
    search_fields = ['nome']
    list_editable = ['ativo']
