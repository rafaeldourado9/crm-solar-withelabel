from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.authtoken.views import obtain_auth_token
from django.views.decorators.csrf import csrf_exempt
from apps.auth_views import me

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/login/', csrf_exempt(obtain_auth_token), name='api-login'),
    path('api/auth/me/', me, name='api-me'),
    path('api/clientes/', include('apps.clientes.urls')),
    path('api/vendedores/', include('apps.vendedores.urls')),
    path('api/premissas/', include('apps.premissas.urls')),
    path('api/equipamentos/', include('apps.equipamentos.urls')),
    path('api/orcamentos/', include('apps.orcamentos.urls')),
    path('api/propostas/', include('apps.propostas.urls')),
    path('api/contratos/', include('apps.contratos.urls')),
    path('api/dashboard/', include('apps.dashboard.urls')),
    path('api/templates/', include('apps.templates.urls')),
    # path('api/ia/', include('apps.ia_urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
