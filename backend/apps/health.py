from django.http import JsonResponse
from django.db import connection
from django.core.cache import cache
import logging

logger = logging.getLogger(__name__)

def health_check(request):
    """Endpoint de health check para monitoramento"""
    status = {
        'status': 'healthy',
        'database': 'unknown',
        'cache': 'unknown',
    }
    
    # Verificar banco de dados
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        status['database'] = 'ok'
    except Exception as e:
        logger.error(f"Database health check failed: {e}")
        status['database'] = 'error'
        status['status'] = 'unhealthy'
    
    # Verificar cache/redis
    try:
        cache.set('health_check', 'ok', 10)
        if cache.get('health_check') == 'ok':
            status['cache'] = 'ok'
        else:
            status['cache'] = 'error'
    except Exception as e:
        logger.error(f"Cache health check failed: {e}")
        status['cache'] = 'error'
    
    http_status = 200 if status['status'] == 'healthy' else 503
    return JsonResponse(status, status=http_status)
