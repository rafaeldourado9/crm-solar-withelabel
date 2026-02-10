import random
from decimal import Decimal
from django.contrib.auth.models import User
from apps.clientes.models import Cliente
from apps.orcamentos.models import Orcamento
from apps.vendedores.models import Vendedor
from apps.equipamentos.models import Painel, Inversor

print("🚀 Iniciando geração de dados em massa...")

# Buscar dados necessários
vendedores = list(Vendedor.objects.all())
paineis = list(Painel.objects.all()[:10])
inversores = list(Inversor.objects.all()[:10])

if not vendedores:
    print("❌ Nenhum vendedor encontrado. Crie pelo menos um vendedor primeiro.")
    exit(1)

if not paineis or not inversores:
    print("❌ Equipamentos não encontrados. Importe painéis e inversores primeiro.")
    exit(1)

cidades = ['Dourados', 'Campo Grande', 'Maracaju', 'Bonito', 'Itaporã', 'Ponta Porã', 
           'Naviraí', 'Caarapó', 'Rio Brilhante', 'Nova Andradina']
estados = ['MS']
nomes = ['João', 'Maria', 'José', 'Ana', 'Pedro', 'Paula', 'Carlos', 'Fernanda', 
         'Ricardo', 'Juliana', 'Roberto', 'Carla', 'Marcos', 'Beatriz', 'Lucas']
sobrenomes = ['Silva', 'Santos', 'Oliveira', 'Souza', 'Lima', 'Costa', 'Pereira', 
              'Rodrigues', 'Almeida', 'Nascimento', 'Ferreira', 'Araújo', 'Ribeiro']

print(f"📊 Criando 3000 clientes...")
clientes_criados = []
batch_size = 100

for i in range(3000):
    nome = f"{random.choice(nomes)} {random.choice(sobrenomes)}"
    cidade = random.choice(cidades)
    vendedor = random.choice(vendedores)
    
    cliente = Cliente(
        nome=nome,
        cidade=cidade,
        estado='MS',
        telefone=f"(67) 9{random.randint(1000,9999)}-{random.randint(1000,9999)}",
        email=f"cliente{i}@teste.com",
        vendedor=vendedor,
        status='orcamento'
    )
    clientes_criados.append(cliente)
    
    if len(clientes_criados) >= batch_size:
        Cliente.objects.bulk_create(clientes_criados)
        print(f"  ✓ {i+1}/3000 clientes criados")
        clientes_criados = []

if clientes_criados:
    Cliente.objects.bulk_create(clientes_criados)

print(f"✅ 3000 clientes criados!")

# Buscar todos os clientes
todos_clientes = list(Cliente.objects.all())
print(f"📊 Criando 10000 orçamentos...")

orcamentos_criados = []
ultimo_numero = Orcamento.objects.count()

for i in range(10000):
    cliente = random.choice(todos_clientes)
    painel = random.choice(paineis)
    inversor = random.choice(inversores)
    
    qtd_paineis = random.randint(8, 20)
    valor_kit = Decimal(random.randint(8000, 15000))
    
    orcamento = Orcamento(
        numero=f"ORC-{ultimo_numero + i + 1:05d}",
        nome_kit=f"Kit {random.randint(5,15)}kWp",
        cliente=cliente,
        vendedor=cliente.vendedor,
        valor_kit=valor_kit,
        marca_painel=painel.fabricante,
        potencia_painel=painel.potencia_w,
        quantidade_paineis=qtd_paineis,
        marca_inversor=inversor.fabricante,
        potencia_inversor=inversor.potencia_w,
        quantidade_inversores=1,
        tipo_estrutura=random.choice(['ceramico', 'fibromadeira', 'laje']),
        valor_estrutura=Decimal(random.randint(0, 500)),
        valor_material_eletrico=Decimal(random.randint(300, 600)),
        valor_total=Decimal(random.randint(10000, 20000)),
        forma_pagamento='avista',
        taxa_juros=Decimal('0'),
        valor_final=Decimal(random.randint(15000, 25000))
    )
    orcamentos_criados.append(orcamento)
    
    if len(orcamentos_criados) >= batch_size:
        Orcamento.objects.bulk_create(orcamentos_criados)
        print(f"  ✓ {i+1}/10000 orçamentos criados")
        orcamentos_criados = []

if orcamentos_criados:
    Orcamento.objects.bulk_create(orcamentos_criados)

print(f"✅ 10000 orçamentos criados!")
print(f"🎉 Geração concluída!")
print(f"📈 Total: {Cliente.objects.count()} clientes, {Orcamento.objects.count()} orçamentos")
