from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AgenteIAViewSet, ConversaIAViewSet

router = DefaultRouter()
router.register(r'agentes', AgenteIAViewSet, basename='agente-ia')
router.register(r'conversas', ConversaIAViewSet, basename='conversa-ia')

urlpatterns = [
    path('', include(router.urls)),
]
