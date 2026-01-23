from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ContratoViewSet

router = DefaultRouter()
router.register(r'', ContratoViewSet)

urlpatterns = [path('', include(router.urls))]
