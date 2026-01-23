from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EquipamentoViewSet, PainelViewSet, InversorViewSet

router = DefaultRouter()
router.register(r'paineis', PainelViewSet)
router.register(r'inversores', InversorViewSet)
router.register(r'', EquipamentoViewSet)

urlpatterns = [path('', include(router.urls))]
