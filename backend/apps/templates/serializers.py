from rest_framework import serializers
from .models import Template
from django.conf import settings

class TemplateSerializer(serializers.ModelSerializer):
    arquivo_url = serializers.SerializerMethodField()
    arquivo_nome = serializers.CharField(required=False, allow_blank=True)
    
    class Meta:
        model = Template
        fields = '__all__'
    
    def get_arquivo_url(self, obj):
        if obj.arquivo:
            return f'http://localhost:8000{obj.arquivo.url}'
        return None
