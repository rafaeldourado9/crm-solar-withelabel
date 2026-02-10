import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.test import TestCase, Client
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from apps.clientes.models import Cliente
from apps.premissas.models import Premissa
import time

class SecurityTests(TestCase):
    """Testes de segurança OWASP"""
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user('test', 'test@test.com', 'Test@123456')
        self.token = Token.objects.create(user=self.user)
        
    def test_security_headers(self):
        """Testa headers de segurança"""
        response = self.client.get('/api/clientes/')
        self.assertEqual(response['X-Content-Type-Options'], 'nosniff')
        self.assertEqual(response['X-Frame-Options'], 'DENY')
        
    def test_rate_limiting(self):
        """Testa rate limiting no login"""
        for i in range(6):
            response = self.client.post('/api/auth/login/', {
                'username': 'wrong',
                'password': 'wrong'
            })
        self.assertEqual(response.status_code, 403)
        
    def test_authentication_required(self):
        """Testa autenticação obrigatória"""
        response = self.client.get('/api/clientes/')
        self.assertEqual(response.status_code, 401)
        
    def test_csrf_protection(self):
        """Testa proteção CSRF"""
        response = self.client.post('/api/clientes/', {})
        self.assertIn(response.status_code, [401, 403])


class IntegrationTests(TestCase):
    """Testes de integração"""
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user('test', 'test@test.com', 'Test@123456')
        self.token = Token.objects.create(user=self.user)
        self.headers = {'HTTP_AUTHORIZATION': f'Token {self.token.key}'}
        
        # Criar premissa padrão
        Premissa.objects.create(
            hsp=5.5,
            perda_sistema=0.20,
            taxa_disponibilidade=0.80,
            margem_lucro=30.0,
            taxa_juros_12x=5.0,
            custo_montagem_kwp=500.0,
            custo_projeto=1500.0
        )
        
    def test_create_cliente(self):
        """Testa criação de cliente"""
        response = self.client.post('/api/clientes/', {
            'nome': 'Cliente Teste',
            'email': 'cliente@teste.com',
            'telefone': '11999999999',
            'cpf_cnpj': '12345678901',
            'tipo_pessoa': 'PF',
            'cep': '01310-100',
            'endereco': 'Av Paulista',
            'numero': '1000',
            'cidade': 'São Paulo',
            'estado': 'SP'
        }, **self.headers)
        self.assertEqual(response.status_code, 201)
        
    def test_list_clientes(self):
        """Testa listagem de clientes"""
        Cliente.objects.create(
            nome='Cliente 1',
            email='c1@test.com',
            telefone='11999999999',
            cpf_cnpj='12345678901',
            tipo_pessoa='PF'
        )
        response = self.client.get('/api/clientes/', **self.headers)
        self.assertEqual(response.status_code, 200)
        self.assertGreater(len(response.json()['results']), 0)
        
    def test_timeout_compliance(self):
        """Testa se requisições respeitam timeout < 3min"""
        start = time.time()
        response = self.client.get('/api/clientes/', **self.headers)
        duration = time.time() - start
        self.assertLess(duration, 180)  # 3 minutos


class PerformanceTests(TestCase):
    """Testes de performance"""
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user('test', 'test@test.com', 'Test@123456')
        self.token = Token.objects.create(user=self.user)
        self.headers = {'HTTP_AUTHORIZATION': f'Token {self.token.key}'}
        
    def test_dashboard_response_time(self):
        """Testa tempo de resposta do dashboard"""
        start = time.time()
        response = self.client.get('/api/dashboard/kpis/', **self.headers)
        duration = time.time() - start
        self.assertEqual(response.status_code, 200)
        self.assertLess(duration, 5)  # Máximo 5 segundos


if __name__ == '__main__':
    import sys
    from django.core.management import execute_from_command_line
    
    print("🧪 Executando testes de segurança e integridade...\n")
    
    sys.argv = ['manage.py', 'test', '--verbosity=2']
    execute_from_command_line(sys.argv)
