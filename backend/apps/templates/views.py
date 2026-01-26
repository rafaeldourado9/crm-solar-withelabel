from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.http import HttpResponse, FileResponse
from .models import Template
from .serializers import TemplateSerializer
import os

class TemplateViewSet(viewsets.ModelViewSet):
    queryset = Template.objects.all()
    serializer_class = TemplateSerializer
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context
    
    def perform_create(self, serializer):
        arquivo = self.request.FILES.get('arquivo')
        serializer.save(arquivo_nome=arquivo.name if arquivo else '')
    
    def retrieve(self, request, pk=None):
        template = self.get_object()
        if 'download' in request.query_params:
            file_path = template.arquivo.path
            if os.path.exists(file_path):
                return FileResponse(open(file_path, 'rb'), as_attachment=True, filename=template.arquivo_nome)
            return Response({'error': 'Arquivo não encontrado'}, status=status.HTTP_404_NOT_FOUND)
        return Response(self.get_serializer(template).data)
    
    @action(detail=True, methods=['post'])
    def converter_com_ia(self, request, pk=None):
        template = self.get_object()
        
        try:
            doc_convertido, mapeamento = IATemplateConverterService.converter_documento(
                template.arquivo.path
            )
            
            buffer = BytesIO()
            doc_convertido.save(buffer)
            buffer.seek(0)
            
            response = HttpResponse(
                buffer.read(),
                content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
            )
            response['Content-Disposition'] = f'attachment; filename="{template.nome}_convertido.docx"'
            
            return response
            
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
