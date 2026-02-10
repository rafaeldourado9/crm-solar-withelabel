# ⚡ Checklist Rápido - Setup FREE (30 min)

## ✅ Passo 1: AWS (10 min)
```
□ Criar conta AWS: https://aws.amazon.com
□ Login console: https://console.aws.amazon.com
□ Região: us-east-1
□ EC2 → Launch Instance:
  □ Name: crm-solar
  □ AMI: Ubuntu 22.04 LTS
  □ Type: t2.micro ✅ FREE
  □ Key pair: Criar e baixar .pem
  □ Security group: SSH(22), HTTP(80), HTTPS(443), 8000
  □ Storage: 30 GB
  □ User data: (copiar do guia)
  □ Launch
□ Copiar IP público: ___________________
```

## ✅ Passo 2: Conectar (5 min)
```bash
# No seu PC
chmod 400 ~/Downloads/crm-solar-key.pem
mv ~/Downloads/crm-solar-key.pem ~/.ssh/
ssh -i ~/.ssh/crm-solar-key.pem ubuntu@SEU_IP
```

## ✅ Passo 3: Instalar (10 min)
```bash
# No servidor EC2
sudo mkdir -p /opt/crm-solar
sudo chown ubuntu:ubuntu /opt/crm-solar
cd /opt/crm-solar

# Clonar
git clone https://github.com/SEU_USUARIO/SunOps---SaaS.git .

# Copiar docker-compose
cp docker-compose.simple.yml docker-compose.yml

# Editar com seu IP
nano docker-compose.yml
# Trocar VITE_API_URL: http://SEU_IP:8000

# Iniciar
docker-compose up -d --build

# Aguardar 2 minutos
sleep 120

# Migrar
docker-compose exec -T backend python manage.py migrate

# Criar admin
docker-compose exec backend python manage.py createsuperuser
```

## ✅ Passo 4: GitHub Actions (5 min)
```bash
# No seu PC - Gerar chave
ssh-keygen -t ed25519 -f ~/.ssh/github_crm
ssh-copy-id -i ~/.ssh/github_crm.pub ubuntu@SEU_IP

# GitHub → Settings → Secrets:
SSH_KEY = [cat ~/.ssh/github_crm]
SERVER_HOST = SEU_IP
SERVER_USER = ubuntu

# Commit workflow
git add .github/workflows/deploy-simple.yml
git commit -m "ci: add deploy"
git push
```

## ✅ Testar
```
□ Frontend: http://SEU_IP
□ Backend: http://SEU_IP:8000/admin
□ Login funciona
□ Criar cliente funciona
□ Push git → Deploy automático funciona
```

## 🎉 PRONTO!

**Custo:** $0/mês (12 meses)
**Usuários:** 20 simultâneos
**Deploy:** Automático

---

## 📞 Comandos Úteis

```bash
# Ver logs
ssh -i ~/.ssh/crm-solar-key.pem ubuntu@SEU_IP
cd /opt/crm-solar
docker-compose logs -f

# Reiniciar
docker-compose restart

# Backup
docker-compose exec -T db pg_dump -U postgres crm_solar > backup.sql

# Limpar espaço
docker system prune -af
```

---

## 🆘 Problemas?

**Servidor lento:**
```bash
# Adicionar swap
sudo fallocate -l 2G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
```

**Sem espaço:**
```bash
docker system prune -af
```

**Deploy falhou:**
```bash
cd /opt/crm-solar
git pull
docker-compose down
docker-compose up -d --build
```

---

**Documentação completa:** [AWS-FREE-SETUP.md](./AWS-FREE-SETUP.md)
