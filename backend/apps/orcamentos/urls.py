from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import OrcamentoViewSet, CalcularMaterialEletricoView, ValidarDimensionamentoView, CalcularDeslocamentoView

router = DefaultRouter()
router.register(r'', OrcamentoViewSet)

urlpatterns = [
    path('validar-dimensionamento/', ValidarDimensionamentoView.as_view(), name='validar-dimensionamento'),
    path('calcular-material-eletrico/', CalcularMaterialEletricoView.as_view(), name='calcular-material-eletrico'),
    path('calcular-deslocamento/', CalcularDeslocamentoView.as_view(), name='calcular-deslocamento'),
    path('', include(router.urls)),
]
