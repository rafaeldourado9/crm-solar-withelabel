# 🆓 Setup AWS 100% GRATUITO - 20 Usuários

## 💰 Arquitetura FREE (Custo: $0/mês)

```
┌─────────────────────────────────────────┐
│  1 EC2 t2.micro (FREE)                  │
│  - Backend + Frontend + PostgreSQL      │
│  - Redis                                │
│  - 1GB RAM, 1 vCPU                      │
│  - 20 usuários simultâneos OK           │
└─────────────────────────────────────────┘
```

**Sem RDS, sem S3, sem CloudFront = $0**

---

## 📋 Passo a Passo Rápido

### 1. Criar Conta AWS (5 min)
```
1. https://aws.amazon.com → Criar conta
2. Adicionar cartão (não será cobrado)
3. Plano: Básico (gratuito)
4. Login: https://console.aws.amazon.com
5. Região: us-east-1 (N. Virginia)
```

### 2. Criar EC2 t2.micro FREE (10 min)
```
Console → EC2 → Launch Instance

NOME:
- crm-solar-free

AMI:
- Ubuntu Server 22.04 LTS (Free tier eligible) ✅

TIPO:
- t2.micro (1 vCPU, 1GB RAM) ✅ FREE

KEY PAIR:
- Create new key pair
- Name: crm-solar-key
- Type: RSA
- Format: .pem
- Download e guardar em ~/.ssh/

NETWORK:
- VPC: default
- Subnet: default
- Auto-assign public IP: Enable ✅

SECURITY GROUP:
- Create security group
- Name: crm-solar-sg
- Rules:
  ✅ SSH (22) - My IP
  ✅ HTTP (80) - Anywhere
  ✅ HTTPS (443) - Anywhere
  ✅ Custom TCP (8000) - Anywhere

STORAGE:
- 30 GB gp3 (FREE até 30GB) ✅

USER DATA (copiar e colar):
```
```bash
#!/bin/bash
apt-get update
apt-get install -y docker.io docker-compose git curl
systemctl start docker
systemctl enable docker
usermod -aG docker ubuntu
```
```
LAUNCH INSTANCE

⏳ Aguardar 2 minutos

Copiar IP público: 54.xxx.xxx.xxx
```

### 3. Conectar e Configurar (15 min)
```bash
# No seu PC
chmod 400 ~/.ssh/crm-solar-key.pem
ssh -i ~/.ssh/crm-solar-key.pem ubuntu@SEU_IP_PUBLICO
```

**No servidor EC2:**
```bash
# Criar estrutura
sudo mkdir -p /opt/crm-solar/.backup
sudo chown -R ubuntu:ubuntu /opt/crm-solar
cd /opt/crm-solar

# Clonar repositório
git clone https://github.com/SEU_USUARIO/SunOps---SaaS.git .
git checkout dev

# Criar docker-compose simplificado
cat > docker-compose.yml << 'EOF'
version: '3.8'

services:
  db:
    image: postgres:15-alpine
    restart: always
    environment:
      POSTGRES_DB: crm_solar
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres123
    volumes:
      - postgres_data:/var/lib/postgresql/data
    networks:
      - crm_network

  redis:
    image: redis:7-alpine
    restart: always
    volumes:
      - redis_data:/data
    networks:
      - crm_network

  backend:
    build: ./backend
    restart: always
    depends_on:
      - db
      - redis
    environment:
      SECRET_KEY: change-this-secret-key-in-production-min-50-chars
      DEBUG: "False"
      ALLOWED_HOSTS: "*"
      DB_NAME: crm_solar
      DB_USER: postgres
      DB_PASSWORD: postgres123
      DB_HOST: db
      DB_PORT: 5432
      REDIS_HOST: redis
      REDIS_PORT: 6379
      CORS_ORIGINS: "*"
    volumes:
      - media_files:/app/media
      - static_files:/app/staticfiles
    ports:
      - "8000:8000"
    networks:
      - crm_network

  frontend:
    build: 
      context: ./frontend
      args:
        VITE_API_URL: http://SEU_IP_PUBLICO:8000
    restart: always
    depends_on:
      - backend
    ports:
      - "80:80"
    networks:
      - crm_network

volumes:
  postgres_data:
  redis_data:
  media_files:
  static_files:

networks:
  crm_network:
    driver: bridge
EOF

# Substituir IP no docker-compose
sed -i "s/SEU_IP_PUBLICO/$(curl -s ifconfig.me)/g" docker-compose.yml

# Criar Dockerfile do backend
cat > backend/Dockerfile << 'EOF'
FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN python manage.py collectstatic --no-input || true

EXPOSE 8000

CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "2"]
EOF

# Criar Dockerfile do frontend
cat > frontend/Dockerfile << 'EOF'
FROM node:18-alpine as build

WORKDIR /app

COPY package*.json ./
RUN npm ci

ARG VITE_API_URL
ENV VITE_API_URL=$VITE_API_URL

COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=build /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
EOF

# Criar nginx.conf
cat > frontend/nginx.conf << 'EOF'
server {
    listen 80;
    server_name _;
    root /usr/share/nginx/html;
    index index.html;

    location / {
        try_files $uri $uri/ /index.html;
    }

    location /api/ {
        proxy_pass http://backend:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
EOF

# Adicionar gunicorn ao requirements.txt
echo "gunicorn==21.2.0" >> backend/requirements.txt

# Build e iniciar
docker-compose up -d --build

# Aguardar containers
echo "⏳ Aguardando containers iniciarem (2 minutos)..."
sleep 120

# Executar migrações
docker-compose exec -T backend python manage.py migrate

# Criar superusuário
echo "Criando superusuário..."
docker-compose exec -T backend python manage.py shell << 'PYEOF'
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    print('Superusuário criado: admin / admin123')
PYEOF

# Verificar
docker-compose ps
curl http://localhost:8000/health/ || echo "Backend ainda iniciando..."

echo ""
echo "✅ INSTALAÇÃO CONCLUÍDA!"
echo ""
echo "🌐 Acesse:"
echo "   Frontend: http://$(curl -s ifconfig.me)"
echo "   Backend:  http://$(curl -s ifconfig.me):8000"
echo "   Admin:    http://$(curl -s ifconfig.me):8000/admin"
echo ""
echo "👤 Login:"
echo "   Usuário: admin"
echo "   Senha: admin123"
echo ""
```

### 4. Configurar GitHub Actions (10 min)

**Gerar chave SSH:**
```bash
# No seu PC
ssh-keygen -t ed25519 -C "github-actions" -f ~/.ssh/github_crm
# Pressionar Enter 3x

# Copiar para servidor
ssh-copy-id -i ~/.ssh/github_crm.pub -o "IdentityFile ~/.ssh/crm-solar-key.pem" ubuntu@SEU_IP

# Ver chave privada (copiar tudo)
cat ~/.ssh/github_crm
```

**GitHub Secrets:**
```
GitHub → Settings → Secrets and variables → Actions

SSH_KEY
Valor: [Colar conteúdo de ~/.ssh/github_crm]

SERVER_HOST
Valor: [IP público do EC2]

SERVER_USER
Valor: ubuntu
```

**Criar workflow simplificado:**
```bash
# No seu PC, na pasta do projeto
mkdir -p .github/workflows

cat > .github/workflows/deploy.yml << 'EOF'
name: Deploy

on:
  push:
    branches: [dev, main]
  workflow_dispatch:

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Deploy to Server
        run: |
          mkdir -p ~/.ssh
          echo "${{ secrets.SSH_KEY }}" > ~/.ssh/id_rsa
          chmod 600 ~/.ssh/id_rsa
          ssh-keyscan -H ${{ secrets.SERVER_HOST }} >> ~/.ssh/known_hosts
          
          ssh ${{ secrets.SERVER_USER }}@${{ secrets.SERVER_HOST }} << 'ENDSSH'
            cd /opt/crm-solar
            git pull origin ${GITHUB_REF##*/}
            docker-compose down
            docker-compose up -d --build
            sleep 30
            docker-compose exec -T backend python manage.py migrate
            docker-compose exec -T backend python manage.py collectstatic --no-input
          ENDSSH
      
      - name: Health Check
        run: |
          sleep 10
          curl -f http://${{ secrets.SERVER_HOST }}:8000/health/ || exit 1
EOF

git add .
git commit -m "feat: add simple CI/CD"
git push origin dev
```

---

## ✅ Pronto! Tudo Funcionando

### Testar:
```
1. Abrir: http://SEU_IP
2. Login: admin / admin123
3. Criar clientes, orçamentos, etc
```

### Deploy automático:
```bash
# Qualquer alteração
git add .
git commit -m "feat: nova funcionalidade"
git push origin dev

# GitHub Actions faz deploy automático!
```

---

## 🔧 Comandos Úteis

```bash
# Conectar ao servidor
ssh -i ~/.ssh/crm-solar-key.pem ubuntu@SEU_IP

# Ver logs
cd /opt/crm-solar
docker-compose logs -f

# Reiniciar
docker-compose restart

# Backup banco
docker-compose exec -T db pg_dump -U postgres crm_solar > backup.sql

# Restaurar banco
docker-compose exec -T db psql -U postgres crm_solar < backup.sql

# Ver uso de recursos
docker stats

# Limpar espaço
docker system prune -af
```

---

## 📊 Limites FREE Tier

```
✅ EC2 t2.micro: 750 horas/mês (24/7 = 720h) = GRÁTIS
✅ 30 GB storage = GRÁTIS
✅ 15 GB transferência/mês = GRÁTIS
✅ 20 usuários simultâneos = OK
✅ Válido por 12 meses

Após 12 meses:
- EC2 t2.micro: ~$8/mês
- Storage 30GB: ~$3/mês
- Total: ~$11/mês
```

---

## 🚀 Melhorias Futuras (Quando crescer)

```
1. Comprar domínio ($12/ano)
2. Adicionar SSL grátis (Let's Encrypt)
3. Upgrade para t2.small ($17/mês)
4. Adicionar RDS ($25/mês)
5. Adicionar S3 + CloudFront ($10/mês)
```

---

## 🆘 Troubleshooting

### Servidor lento?
```bash
# Adicionar swap
sudo fallocate -l 2G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab
```

### Sem espaço?
```bash
docker system prune -af
docker volume prune -f
```

### Deploy falhou?
```bash
cd /opt/crm-solar
git pull origin dev
docker-compose down
docker-compose up -d --build
```

---

## 📞 Resumo

**Tempo total:** 30 minutos
**Custo:** $0/mês (12 meses)
**Capacidade:** 20 usuários simultâneos
**Backup:** Manual (comando acima)
**Deploy:** Automático via GitHub Actions

**Pronto para produção!** 🎉
