from django.contrib import admin
from .models import AgenteIA, ConversaIA


@admin.register(AgenteIA)
class AgenteIAAdmin(admin.ModelAdmin):
    list_display = ['id', 'vendedor', 'nome_agente', 'criado_em']
    search_fields = ['vendedor__username', 'nome_agente']
    list_filter = ['criado_em']


@admin.register(ConversaIA)
class ConversaIAAdmin(admin.ModelAdmin):
    list_display = ['id', 'vendedor', 'tipo_acao', 'criado_em']
    search_fields = ['vendedor__username', 'mensagem', 'resposta']
    list_filter = ['tipo_acao', 'criado_em']
    readonly_fields = ['criado_em']
