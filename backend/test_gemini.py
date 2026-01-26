import google.generativeai as genai
import os

# Configurar API
API_KEY = "AIzaSyDGg9yLvo9GiRz3tRsbu5LyMrMg01zLMMk"
genai.configure(api_key=API_KEY)

print("=" * 50)
print("TESTE DE CONEXÃO COM GEMINI API")
print("=" * 50)
print()

try:
    # Listar modelos disponíveis
    print("1. Listando modelos disponíveis...")
    for model in genai.list_models():
        if 'generateContent' in model.supported_generation_methods:
            print(f"   ✓ {model.name}")
    print()
    
    # Testar geração de conteúdo
    print("2. Testando geração de conteúdo...")
    model = genai.GenerativeModel('gemini-2.0-flash-exp')
    
    response = model.generate_content("Diga apenas 'API funcionando!' em português")
    print(f"   Resposta: {response.text}")
    print()
    
    print("=" * 50)
    print("✓ TODOS OS TESTES PASSARAM!")
    print("=" * 50)
    
except Exception as e:
    print()
    print("=" * 50)
    print("✗ ERRO NA CONEXÃO!")
    print("=" * 50)
    print(f"Erro: {e}")
