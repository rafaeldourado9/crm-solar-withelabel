# Deploy AWS - CRM Solar

## 🎯 Arquitetura (Barata e Escalável)

### Recursos AWS
- **EC2 t3.micro** (2 instâncias): Dev + Prod - ~$15/mês
- **RDS PostgreSQL t3.micro**: Banco gerenciado - ~$15/mês
- **S3**: Armazenamento de PDFs/arquivos - ~$1/mês
- **CloudFront**: CDN para frontend - ~$1/mês
- **Route53**: DNS - ~$1/mês
- **Elastic IP**: 2 IPs fixos - Grátis (se anexado)

**CUSTO TOTAL: ~$33/mês** (para 10 admins + 15 vendedores + 5 DAU)

---

## 📦 Estrutura de Ambientes

```
┌─────────────────────────────────────────────────────┐
│                    PRODUÇÃO                         │
│  EC2 t3.micro (prod.sunops.com.br)                 │
│  - Docker Compose (Django + React)                  │
│  - Nginx Reverse Proxy                              │
│  - SSL Let's Encrypt                                │
│  - RDS PostgreSQL (prod)                            │
└─────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────┐
│                 DESENVOLVIMENTO                      │
│  EC2 t3.micro (dev.sunops.com.br)                  │
│  - Docker Compose (Django + React)                  │
│  - RDS PostgreSQL (dev)                             │
└─────────────────────────────────────────────────────┘
```

---

## 🚀 CI/CD com GitHub Actions

### Fluxo Automático

1. **Push para `develop`** → Deploy automático em DEV
2. **Push para `main`** → Deploy automático em PROD
3. **Rollback** → Revert commit + redeploy automático
4. **Backup** → Diário automático às 3h AM

---

## 📝 Setup Inicial

### 1. Criar Infraestrutura AWS

```bash
# 1.1 - Criar VPC e Security Groups
aws ec2 create-security-group \
  --group-name sunops-sg \
  --description "CRM Solar Security Group"

# Liberar portas
aws ec2 authorize-security-group-ingress \
  --group-name sunops-sg \
  --protocol tcp --port 22 --cidr 0.0.0.0/0  # SSH
aws ec2 authorize-security-group-ingress \
  --group-name sunops-sg \
  --protocol tcp --port 80 --cidr 0.0.0.0/0  # HTTP
aws ec2 authorize-security-group-ingress \
  --group-name sunops-sg \
  --protocol tcp --port 443 --cidr 0.0.0.0/0 # HTTPS

# 1.2 - Criar RDS PostgreSQL
aws rds create-db-instance \
  --db-instance-identifier sunops-db-prod \
  --db-instance-class db.t3.micro \
  --engine postgres \
  --master-username sunops \
  --master-user-password SENHA_FORTE_AQUI \
  --allocated-storage 20 \
  --backup-retention-period 7 \
  --vpc-security-group-ids sg-xxxxx

# 1.3 - Criar EC2 (Prod)
aws ec2 run-instances \
  --image-id ami-0c55b159cbfafe1f0 \
  --instance-type t3.micro \
  --key-name sunops-key \
  --security-group-ids sg-xxxxx \
  --tag-specifications 'ResourceType=instance,Tags=[{Key=Name,Value=sunops-prod}]'

# 1.4 - Criar EC2 (Dev)
aws ec2 run-instances \
  --image-id ami-0c55b159cbfafe1f0 \
  --instance-type t3.micro \
  --key-name sunops-key \
  --security-group-ids sg-xxxxx \
  --tag-specifications 'ResourceType=instance,Tags=[{Key=Name,Value=sunops-dev}]'

# 1.5 - Criar S3 Bucket
aws s3 mb s3://sunops-storage
aws s3api put-bucket-versioning \
  --bucket sunops-storage \
  --versioning-configuration Status=Enabled
```

---

### 2. Configurar Servidores EC2

```bash
# SSH no servidor
ssh -i sunops-key.pem ubuntu@IP_DO_SERVIDOR

# Instalar Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker ubuntu

# Instalar Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Criar diretórios
mkdir -p /home/ubuntu/sunops/{backend,frontend,nginx,backups}
```

---

## 🔧 Arquivos de Configuração

### docker-compose.prod.yml

```yaml
version: '3.8'

services:
  backend:
    image: ghcr.io/seu-usuario/sunops-backend:latest
    container_name: sunops-backend
    restart: always
    env_file:
      - .env.prod
    volumes:
      - static_volume:/app/staticfiles
      - media_volume:/app/media
    networks:
      - sunops-network
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health/"]
      interval: 30s
      timeout: 10s
      retries: 3

  frontend:
    image: ghcr.io/seu-usuario/sunops-frontend:latest
    container_name: sunops-frontend
    restart: always
    networks:
      - sunops-network

  nginx:
    image: nginx:alpine
    container_name: sunops-nginx
    restart: always
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/nginx.conf:ro
      - ./nginx/ssl:/etc/nginx/ssl:ro
      - static_volume:/var/www/static:ro
      - media_volume:/var/www/media:ro
    depends_on:
      - backend
      - frontend
    networks:
      - sunops-network

volumes:
  static_volume:
  media_volume:

networks:
  sunops-network:
    driver: bridge
```

---

### .env.prod

```bash
# Django
DEBUG=False
SECRET_KEY=sua-secret-key-super-segura-aqui
ALLOWED_HOSTS=prod.sunops.com.br,sunops.com.br

# Database
DATABASE_URL=postgresql://sunops:senha@sunops-db-prod.xxxxx.rds.amazonaws.com:5432/sunops

# AWS S3
AWS_ACCESS_KEY_ID=AKIAXXXXXXXX
AWS_SECRET_ACCESS_KEY=xxxxxxxx
AWS_STORAGE_BUCKET_NAME=sunops-storage
AWS_S3_REGION_NAME=us-east-1

# Email (SES)
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=email-smtp.us-east-1.amazonaws.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=AKIAXXXXXXXX
EMAIL_HOST_PASSWORD=xxxxxxxx

# Gemini (opcional)
GEMINI_API_KEY=sua-key-aqui

# Google Maps (opcional)
GOOGLE_MAPS_API_KEY=sua-key-aqui
```

---

### nginx/nginx.conf

```nginx
events {
    worker_connections 1024;
}

http {
    upstream backend {
        server backend:8000;
    }

    upstream frontend {
        server frontend:80;
    }

    # Redirect HTTP to HTTPS
    server {
        listen 80;
        server_name sunops.com.br www.sunops.com.br;
        return 301 https://$server_name$request_uri;
    }

    # HTTPS Server
    server {
        listen 443 ssl http2;
        server_name sunops.com.br www.sunops.com.br;

        ssl_certificate /etc/nginx/ssl/fullchain.pem;
        ssl_certificate_key /etc/nginx/ssl/privkey.pem;
        ssl_protocols TLSv1.2 TLSv1.3;
        ssl_ciphers HIGH:!aNULL:!MD5;

        client_max_body_size 50M;

        # Frontend
        location / {
            proxy_pass http://frontend;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }

        # Backend API
        location /api/ {
            proxy_pass http://backend;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }

        # Django Admin
        location /admin/ {
            proxy_pass http://backend;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
        }

        # Static files
        location /static/ {
            alias /var/www/static/;
            expires 30d;
            add_header Cache-Control "public, immutable";
        }

        # Media files
        location /media/ {
            alias /var/www/media/;
            expires 7d;
        }
    }
}
```

---

## 🤖 GitHub Actions CI/CD

### .github/workflows/deploy-dev.yml

```yaml
name: Deploy DEV

on:
  push:
    branches: [develop]

jobs:
  deploy:
    runs-on: ubuntu-latest
    
    steps:
      - name: Checkout code
        uses: actions/checkout@v3

      - name: Build Backend Image
        run: |
          docker build -t ghcr.io/${{ github.repository }}/backend:dev ./backend
          echo ${{ secrets.GITHUB_TOKEN }} | docker login ghcr.io -u ${{ github.actor }} --password-stdin
          docker push ghcr.io/${{ github.repository }}/backend:dev

      - name: Build Frontend Image
        run: |
          docker build -t ghcr.io/${{ github.repository }}/frontend:dev ./frontend
          docker push ghcr.io/${{ github.repository }}/frontend:dev

      - name: Deploy to DEV Server
        uses: appleboy/ssh-action@master
        with:
          host: ${{ secrets.DEV_HOST }}
          username: ubuntu
          key: ${{ secrets.SSH_PRIVATE_KEY }}
          script: |
            cd /home/ubuntu/sunops
            docker-compose -f docker-compose.dev.yml pull
            docker-compose -f docker-compose.dev.yml up -d
            docker-compose -f docker-compose.dev.yml exec -T backend python manage.py migrate
            docker-compose -f docker-compose.dev.yml exec -T backend python manage.py collectstatic --noinput

      - name: Health Check
        run: |
          sleep 10
          curl -f https://dev.sunops.com.br/health/ || exit 1

      - name: Notify Slack
        if: always()
        uses: 8398a7/action-slack@v3
        with:
          status: ${{ job.status }}
          text: 'Deploy DEV: ${{ job.status }}'
          webhook_url: ${{ secrets.SLACK_WEBHOOK }}
```

---

### .github/workflows/deploy-prod.yml

```yaml
name: Deploy PROD

on:
  push:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
      - name: Checkout code
        uses: actions/checkout@v3

      - name: Run Tests
        run: |
          cd backend
          docker-compose -f docker-compose.test.yml up --abort-on-container-exit
          docker-compose -f docker-compose.test.yml down

  deploy:
    needs: test
    runs-on: ubuntu-latest
    
    steps:
      - name: Checkout code
        uses: actions/checkout@v3

      - name: Build Backend Image
        run: |
          docker build -t ghcr.io/${{ github.repository }}/backend:latest ./backend
          docker tag ghcr.io/${{ github.repository }}/backend:latest ghcr.io/${{ github.repository }}/backend:${{ github.sha }}
          echo ${{ secrets.GITHUB_TOKEN }} | docker login ghcr.io -u ${{ github.actor }} --password-stdin
          docker push ghcr.io/${{ github.repository }}/backend:latest
          docker push ghcr.io/${{ github.repository }}/backend:${{ github.sha }}

      - name: Build Frontend Image
        run: |
          docker build -t ghcr.io/${{ github.repository }}/frontend:latest ./frontend
          docker tag ghcr.io/${{ github.repository }}/frontend:latest ghcr.io/${{ github.repository }}/frontend:${{ github.sha }}
          docker push ghcr.io/${{ github.repository }}/frontend:latest
          docker push ghcr.io/${{ github.repository }}/frontend:${{ github.sha }}

      - name: Backup Database
        uses: appleboy/ssh-action@master
        with:
          host: ${{ secrets.PROD_HOST }}
          username: ubuntu
          key: ${{ secrets.SSH_PRIVATE_KEY }}
          script: |
            cd /home/ubuntu/sunops
            ./scripts/backup.sh

      - name: Deploy to PROD Server
        uses: appleboy/ssh-action@master
        with:
          host: ${{ secrets.PROD_HOST }}
          username: ubuntu
          key: ${{ secrets.SSH_PRIVATE_KEY }}
          script: |
            cd /home/ubuntu/sunops
            docker-compose -f docker-compose.prod.yml pull
            docker-compose -f docker-compose.prod.yml up -d
            docker-compose -f docker-compose.prod.yml exec -T backend python manage.py migrate
            docker-compose -f docker-compose.prod.yml exec -T backend python manage.py collectstatic --noinput

      - name: Health Check
        run: |
          sleep 15
          curl -f https://sunops.com.br/health/ || exit 1

      - name: Notify Slack
        if: always()
        uses: 8398a7/action-slack@v3
        with:
          status: ${{ job.status }}
          text: 'Deploy PROD: ${{ job.status }}'
          webhook_url: ${{ secrets.SLACK_WEBHOOK }}
```

---

### .github/workflows/rollback.yml

```yaml
name: Rollback PROD

on:
  workflow_dispatch:
    inputs:
      commit_sha:
        description: 'Commit SHA to rollback to'
        required: true

jobs:
  rollback:
    runs-on: ubuntu-latest
    
    steps:
      - name: Backup Current State
        uses: appleboy/ssh-action@master
        with:
          host: ${{ secrets.PROD_HOST }}
          username: ubuntu
          key: ${{ secrets.SSH_PRIVATE_KEY }}
          script: |
            cd /home/ubuntu/sunops
            ./scripts/backup.sh emergency

      - name: Rollback to Previous Version
        uses: appleboy/ssh-action@master
        with:
          host: ${{ secrets.PROD_HOST }}
          username: ubuntu
          key: ${{ secrets.SSH_PRIVATE_KEY }}
          script: |
            cd /home/ubuntu/sunops
            docker-compose -f docker-compose.prod.yml down
            docker pull ghcr.io/${{ github.repository }}/backend:${{ github.event.inputs.commit_sha }}
            docker pull ghcr.io/${{ github.repository }}/frontend:${{ github.event.inputs.commit_sha }}
            docker tag ghcr.io/${{ github.repository }}/backend:${{ github.event.inputs.commit_sha }} ghcr.io/${{ github.repository }}/backend:latest
            docker tag ghcr.io/${{ github.repository }}/frontend:${{ github.event.inputs.commit_sha }} ghcr.io/${{ github.repository }}/frontend:latest
            docker-compose -f docker-compose.prod.yml up -d

      - name: Health Check
        run: |
          sleep 15
          curl -f https://sunops.com.br/health/ || exit 1

      - name: Notify Slack
        uses: 8398a7/action-slack@v3
        with:
          status: 'warning'
          text: 'ROLLBACK executado para commit ${{ github.event.inputs.commit_sha }}'
          webhook_url: ${{ secrets.SLACK_WEBHOOK }}
```

---

## 💾 Scripts de Backup

### scripts/backup.sh

```bash
#!/bin/bash

BACKUP_DIR="/home/ubuntu/sunops/backups"
DATE=$(date +%Y%m%d_%H%M%S)
S3_BUCKET="s3://sunops-backups"

# Backup Database
docker-compose -f docker-compose.prod.yml exec -T backend python manage.py dumpdata \
  --exclude auth.permission \
  --exclude contenttypes \
  --indent 2 > "$BACKUP_DIR/db_$DATE.json"

# Backup Media Files
tar -czf "$BACKUP_DIR/media_$DATE.tar.gz" /home/ubuntu/sunops/media/

# Upload to S3
aws s3 cp "$BACKUP_DIR/db_$DATE.json" "$S3_BUCKET/db/"
aws s3 cp "$BACKUP_DIR/media_$DATE.tar.gz" "$S3_BUCKET/media/"

# Keep only last 7 days locally
find "$BACKUP_DIR" -name "*.json" -mtime +7 -delete
find "$BACKUP_DIR" -name "*.tar.gz" -mtime +7 -delete

echo "Backup completed: $DATE"
```

---

### scripts/restore.sh

```bash
#!/bin/bash

if [ -z "$1" ]; then
  echo "Usage: ./restore.sh BACKUP_DATE (ex: 20240123_030000)"
  exit 1
fi

BACKUP_DATE=$1
BACKUP_DIR="/home/ubuntu/sunops/backups"
S3_BUCKET="s3://sunops-backups"

# Download from S3
aws s3 cp "$S3_BUCKET/db/db_$BACKUP_DATE.json" "$BACKUP_DIR/"
aws s3 cp "$S3_BUCKET/media/media_$BACKUP_DATE.tar.gz" "$BACKUP_DIR/"

# Restore Database
docker-compose -f docker-compose.prod.yml exec -T backend python manage.py flush --noinput
docker-compose -f docker-compose.prod.yml exec -T backend python manage.py loaddata "$BACKUP_DIR/db_$BACKUP_DATE.json"

# Restore Media
tar -xzf "$BACKUP_DIR/media_$BACKUP_DATE.tar.gz" -C /

echo "Restore completed: $BACKUP_DATE"
```

---

## 🔐 Secrets do GitHub

Configure no GitHub: `Settings > Secrets and variables > Actions`

```
DEV_HOST=dev.sunops.com.br
PROD_HOST=sunops.com.br
SSH_PRIVATE_KEY=<conteúdo da chave privada>
SLACK_WEBHOOK=https://hooks.slack.com/services/xxx
AWS_ACCESS_KEY_ID=AKIAXXXXXXXX
AWS_SECRET_ACCESS_KEY=xxxxxxxx
```

---

## 📊 Monitoramento

### Health Check Endpoint

```python
# backend/apps/core/views.py
from django.http import JsonResponse
from django.db import connection

def health_check(request):
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        return JsonResponse({"status": "healthy", "database": "ok"})
    except Exception as e:
        return JsonResponse({"status": "unhealthy", "error": str(e)}, status=500)
```

---

## 🚀 Deploy Manual (Primeira Vez)

```bash
# 1. SSH no servidor
ssh -i sunops-key.pem ubuntu@IP_PROD

# 2. Clonar repositório
git clone https://github.com/seu-usuario/sunops.git /home/ubuntu/sunops
cd /home/ubuntu/sunops

# 3. Configurar .env
cp .env.example .env.prod
nano .env.prod  # Editar variáveis

# 4. SSL com Let's Encrypt
sudo apt install certbot
sudo certbot certonly --standalone -d sunops.com.br -d www.sunops.com.br
sudo cp /etc/letsencrypt/live/sunops.com.br/fullchain.pem nginx/ssl/
sudo cp /etc/letsencrypt/live/sunops.com.br/privkey.pem nginx/ssl/

# 5. Subir aplicação
docker-compose -f docker-compose.prod.yml up -d

# 6. Migrations e superuser
docker-compose -f docker-compose.prod.yml exec backend python manage.py migrate
docker-compose -f docker-compose.prod.yml exec backend python manage.py createsuperuser

# 7. Configurar backup automático
crontab -e
# Adicionar: 0 3 * * * /home/ubuntu/sunops/scripts/backup.sh
```

---

## 📈 Escalabilidade Futura

Se crescer além de 25 usuários:

1. **Upgrade EC2**: t3.micro → t3.small (~$30/mês)
2. **Load Balancer**: ALB para múltiplas instâncias (~$20/mês)
3. **RDS Multi-AZ**: Alta disponibilidade (~$30/mês)
4. **ElastiCache Redis**: Cache de sessões (~$15/mês)

---

## 🎯 Checklist de Deploy

- [ ] Criar infraestrutura AWS (VPC, EC2, RDS, S3)
- [ ] Configurar DNS no Route53
- [ ] Instalar Docker nos servidores
- [ ] Configurar SSL com Let's Encrypt
- [ ] Configurar secrets no GitHub
- [ ] Fazer primeiro deploy manual
- [ ] Testar CI/CD (push para develop)
- [ ] Testar backup/restore
- [ ] Configurar monitoramento
- [ ] Documentar credenciais (1Password/Vault)

---

## 💰 Otimização de Custos

- **Reserved Instances**: Economize 40% comprando 1 ano
- **S3 Lifecycle**: Mover backups antigos para Glacier
- **CloudWatch Alarms**: Alertas de uso excessivo
- **Auto Shutdown**: Desligar DEV à noite (economiza 50%)

**Custo otimizado: ~$25/mês**
