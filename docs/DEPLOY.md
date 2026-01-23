# Guia de Deploy - Produção

## Pré-requisitos

- Servidor Linux (Ubuntu 20.04+)
- Docker & Docker Compose
- Domínio configurado
- Certificado SSL (Let's Encrypt)

## Variáveis de Ambiente

Crie arquivo `.env` na raiz:

```env
# Django
SECRET_KEY=sua-chave-secreta-aqui
DEBUG=False
ALLOWED_HOSTS=seudominio.com,www.seudominio.com

# Database
DB_NAME=crm_solar_prod
DB_USER=crm_user
DB_PASSWORD=senha-forte-aqui
DB_HOST=db
DB_PORT=5432

# CORS
CORS_ORIGINS=https://seudominio.com

# OpenAI (opcional)
OPENAI_API_KEY=sk-...
```

## Docker Compose - Produção

Use `docker-compose.prod.yml`:

```yaml
version: '3.8'

services:
  db:
    image: postgres:15
    environment:
      POSTGRES_DB: ${DB_NAME}
      POSTGRES_USER: ${DB_USER}
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    restart: always

  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile.prod
    command: gunicorn config.wsgi:application --bind 0.0.0.0:8000
    volumes:
      - static_volume:/app/staticfiles
      - media_volume:/app/media
    environment:
      - SECRET_KEY=${SECRET_KEY}
      - DEBUG=${DEBUG}
      - ALLOWED_HOSTS=${ALLOWED_HOSTS}
      - DB_NAME=${DB_NAME}
      - DB_USER=${DB_USER}
      - DB_PASSWORD=${DB_PASSWORD}
      - DB_HOST=${DB_HOST}
    depends_on:
      - db
    restart: always

  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile.prod
    restart: always

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx/nginx.prod.conf:/etc/nginx/nginx.conf
      - static_volume:/static
      - media_volume:/media
      - ./certbot/conf:/etc/letsencrypt
      - ./certbot/www:/var/www/certbot
    depends_on:
      - backend
      - frontend
    restart: always

volumes:
  postgres_data:
  static_volume:
  media_volume:
```

## Passos de Deploy

### 1. Preparar Servidor

```bash
# Atualizar sistema
sudo apt update && sudo apt upgrade -y

# Instalar Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Instalar Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

### 2. Clonar Repositório

```bash
git clone <repo-url> /var/www/crm-solar
cd /var/www/crm-solar
```

### 3. Configurar Ambiente

```bash
# Copiar .env de exemplo
cp .env.example .env

# Editar com valores de produção
nano .env
```

### 4. Build e Deploy

```bash
# Build das imagens
docker-compose -f docker-compose.prod.yml build

# Subir containers
docker-compose -f docker-compose.prod.yml up -d

# Executar migrações
docker-compose -f docker-compose.prod.yml exec backend python manage.py migrate

# Criar superuser
docker-compose -f docker-compose.prod.yml exec backend python manage.py createsuperuser

# Coletar arquivos estáticos
docker-compose -f docker-compose.prod.yml exec backend python manage.py collectstatic --noinput
```

### 5. Configurar SSL (Let's Encrypt)

```bash
# Instalar Certbot
sudo apt install certbot python3-certbot-nginx

# Obter certificado
sudo certbot --nginx -d seudominio.com -d www.seudominio.com

# Renovação automática
sudo certbot renew --dry-run
```

## Nginx - Configuração Produção

```nginx
upstream backend {
    server backend:8000;
}

upstream frontend {
    server frontend:3000;
}

server {
    listen 80;
    server_name seudominio.com www.seudominio.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name seudominio.com www.seudominio.com;

    ssl_certificate /etc/letsencrypt/live/seudominio.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/seudominio.com/privkey.pem;

    location /api/ {
        proxy_pass http://backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /admin/ {
        proxy_pass http://backend;
        proxy_set_header Host $host;
    }

    location /static/ {
        alias /static/;
    }

    location /media/ {
        alias /media/;
    }

    location / {
        proxy_pass http://frontend;
        proxy_set_header Host $host;
    }
}
```

## Backup

### Banco de Dados

```bash
# Backup manual
docker-compose exec db pg_dump -U crm_user crm_solar_prod > backup_$(date +%Y%m%d).sql

# Restaurar
docker-compose exec -T db psql -U crm_user crm_solar_prod < backup_20260123.sql
```

### Automatizar Backup (Cron)

```bash
# Editar crontab
crontab -e

# Adicionar linha (backup diário às 2h)
0 2 * * * cd /var/www/crm-solar && docker-compose exec -T db pg_dump -U crm_user crm_solar_prod > /backups/backup_$(date +\%Y\%m\%d).sql
```

## Monitoramento

### Logs

```bash
# Ver logs em tempo real
docker-compose logs -f backend

# Últimas 100 linhas
docker-compose logs --tail=100 backend
```

### Health Check

```bash
# Verificar status
docker-compose ps

# Testar API
curl https://seudominio.com/api/dashboard/resumo/
```

## Atualizações

```bash
# Pull do código
git pull origin main

# Rebuild
docker-compose -f docker-compose.prod.yml build

# Restart
docker-compose -f docker-compose.prod.yml up -d

# Migrações
docker-compose -f docker-compose.prod.yml exec backend python manage.py migrate
```

## Rollback

```bash
# Voltar para commit anterior
git checkout <commit-hash>

# Rebuild e restart
docker-compose -f docker-compose.prod.yml build
docker-compose -f docker-compose.prod.yml up -d
```

## Troubleshooting

### Container não inicia
```bash
docker-compose logs backend
```

### Erro de permissão
```bash
sudo chown -R $USER:$USER /var/www/crm-solar
```

### Banco não conecta
```bash
docker-compose exec backend python manage.py dbshell
```

## Segurança

- [ ] Firewall configurado (UFW)
- [ ] SSH com chave pública
- [ ] Fail2ban instalado
- [ ] Backups automáticos
- [ ] SSL ativo
- [ ] Senhas fortes
- [ ] SECRET_KEY único
- [ ] DEBUG=False
