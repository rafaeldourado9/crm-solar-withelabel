from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PremissaViewSet

router = DefaultRouter()
router.register(r'', PremissaViewSet)

urlpatterns = [path('', include(router.urls))]
