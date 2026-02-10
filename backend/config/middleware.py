from django.db import connection
from django.http import JsonResponse
import logging

logger = logging.getLogger(__name__)

class DatabaseFallbackMiddleware:
    """Middleware para detectar falhas de conexão com banco e retornar resposta apropriada"""
    
    def __init__(self, get_response):
        self.get_response = get_response
        
    def __call__(self, request):
        try:
            # Tenta executar a requisição normalmente
            response = self.get_response(request)
            return response
        except Exception as e:
            # Se for erro de conexão com banco
            if 'connection' in str(e).lower() or 'database' in str(e).lower():
                logger.error(f"Database connection failed: {e}")
                return JsonResponse({
                    'error': 'Database temporarily unavailable',
                    'message': 'Sistema em manutenção. Tente novamente em alguns minutos.',
                    'status': 'maintenance'
                }, status=503)
            raise

    def process_exception(self, request, exception):
        """Captura exceções de banco de dados"""
        if 'connection' in str(exception).lower() or 'database' in str(exception).lower():
            logger.error(f"Database exception: {exception}")
            return JsonResponse({
                'error': 'Database error',
                'message': 'Erro de conexão com banco de dados',
                'status': 'error'
            }, status=503)
        return None
