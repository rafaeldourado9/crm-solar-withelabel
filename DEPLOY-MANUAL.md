# 🚀 DEPLOY MANUAL - 5 PASSOS

## ✅ Você tem:
- EC2: i-07a9e55abd9e8a7be
- Região: us-east-1
- Credenciais AWS configuradas

---

## 📋 EXECUTE:

### 1. Obter IP do EC2
Acesse: https://console.aws.amazon.com/ec2/
- Procure instância: i-07a9e55abd9e8a7be
- Copie o "Public IPv4 address"

**OU via AWS CLI:**
```bash
aws ec2 describe-instances --instance-ids i-07a9e55abd9e8a7be --query 'Reservations[0].Instances[0].PublicIpAddress' --output text
```

### 2. Liberar portas no Security Group
No console AWS:
- EC2 > Security Groups
- Selecione o SG da instância
- Inbound rules > Edit
- Adicionar:
  - HTTP (80) - 0.0.0.0/0
  - HTTPS (443) - 0.0.0.0/0
  - SSH (22) - Seu IP

### 3. Conectar via SSH
```bash
ssh -i sua-chave.pem ubuntu@SEU-EC2-IP
```

### 4. Executar deploy no EC2
```bash
# Instalar Git
sudo apt-get update
sudo apt-get install -y git

# Clonar repo
git clone https://github.com/SEU-USUARIO/SunOps---SaaS.git /tmp/crm
cd /tmp/crm

# Executar script
chmod +x scripts/deploy-ec2-full.sh
sudo ./scripts/deploy-ec2-full.sh
```

### 5. Acessar
```
http://SEU-EC2-IP
http://SEU-EC2-IP/admin

User: admin
Pass: Admin@123456
```

---

## 🆘 SE NÃO TIVER AWS CLI:

### Windows (PowerShell):
```powershell
.\scripts\setup-ec2.ps1
```

### Ou faça tudo manual pelo console AWS! 👆

---

## ⏱️ Tempo total: ~10 minutos
- 2 min: Configurar SG
- 1 min: Conectar SSH
- 7 min: Deploy automático
