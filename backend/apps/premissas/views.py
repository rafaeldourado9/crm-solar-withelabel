from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Premissa
from .serializers import PremissaSerializer

class PremissaViewSet(viewsets.ModelViewSet):
    queryset = Premissa.objects.all()
    serializer_class = PremissaSerializer
    
    @action(detail=False, methods=['get'])
    def ativa(self, request):
        premissa = Premissa.get_ativa()
        return Response(PremissaSerializer(premissa).data)
