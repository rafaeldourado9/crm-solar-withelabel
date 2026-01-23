# 🐳 Docker - CRM Solar

## Desenvolvimento

```bash
# Iniciar todos os serviços
docker-compose up -d

# Ver logs
docker-compose logs -f

# Parar serviços
docker-compose down

# Rebuild
docker-compose up -d --build
```

**Acessos:**
- Frontend: http://localhost:5173
- Backend: http://localhost:8000
- Admin: http://localhost:8000/admin

## Produção

```bash
# Build e iniciar
docker-compose -f docker-compose.prod.yml up -d --build

# Ver logs
docker-compose -f docker-compose.prod.yml logs -f

# Parar
docker-compose -f docker-compose.prod.yml down
```

**Acesso:** http://localhost

## Comandos Úteis

```bash
# Criar superusuário
docker-compose exec backend python manage.py createsuperuser

# Migrations
docker-compose exec backend python manage.py makemigrations
docker-compose exec backend python manage.py migrate

# Shell Django
docker-compose exec backend python manage.py shell

# Logs específicos
docker-compose logs -f backend
docker-compose logs -f frontend
docker-compose logs -f db
```

## Estrutura

```
crm_solar/
├── backend/
│   ├── Dockerfile          # Dev
│   ├── Dockerfile.prod     # Produção
│   └── entrypoint.sh       # Script inicialização
├── frontend/
│   ├── Dockerfile          # Dev
│   └── Dockerfile.prod     # Produção
├── nginx/
│   └── nginx.prod.conf     # Config Nginx
├── docker-compose.yml      # Dev
└── docker-compose.prod.yml # Produção
```
