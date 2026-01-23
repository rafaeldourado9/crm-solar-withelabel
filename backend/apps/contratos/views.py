from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Contrato
from .serializers import ContratoSerializer

class ContratoViewSet(viewsets.ModelViewSet):
    queryset = Contrato.objects.all()
    serializer_class = ContratoSerializer
    
    @action(detail=True, methods=['post'])
    def gerar_pdf(self, request, pk=None):
        contrato = self.get_object()
        # TODO: Implementar geração de PDF do contrato
        return Response({'message': 'PDF gerado'})
