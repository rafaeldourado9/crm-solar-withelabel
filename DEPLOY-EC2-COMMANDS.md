# 🚀 DEPLOY NO EC2 - COMANDOS

## 1️⃣ Obter IP do EC2
```bash
aws ec2 describe-instances \
  --instance-ids i-07a9e55abd9e8a7be \
  --query 'Reservations[0].Instances[0].PublicIpAddress' \
  --output text
```

## 2️⃣ Obter chave SSH (se não tiver)
```bash
# Listar chaves disponíveis
aws ec2 describe-key-pairs --query 'KeyPairs[*].KeyName'

# Se precisar criar nova
aws ec2 create-key-pair \
  --key-name crm-solar-key \
  --query 'KeyMaterial' \
  --output text > crm-solar-key.pem
chmod 400 crm-solar-key.pem
```

## 3️⃣ Configurar Security Group
```bash
# Obter Security Group ID
SG_ID=$(aws ec2 describe-instances \
  --instance-ids i-07a9e55abd9e8a7be \
  --query 'Reservations[0].Instances[0].SecurityGroups[0].GroupId' \
  --output text)

# Adicionar regras
aws ec2 authorize-security-group-ingress \
  --group-id $SG_ID \
  --protocol tcp \
  --port 80 \
  --cidr 0.0.0.0/0

aws ec2 authorize-security-group-ingress \
  --group-id $SG_ID \
  --protocol tcp \
  --port 443 \
  --cidr 0.0.0.0/0

aws ec2 authorize-security-group-ingress \
  --group-id $SG_ID \
  --protocol tcp \
  --port 22 \
  --cidr 0.0.0.0/0
```

## 4️⃣ Conectar e Deploy
```bash
# Obter IP
EC2_IP=$(aws ec2 describe-instances \
  --instance-ids i-07a9e55abd9e8a7be \
  --query 'Reservations[0].Instances[0].PublicIpAddress' \
  --output text)

# Conectar
ssh -i sua-chave.pem ubuntu@$EC2_IP

# No EC2, executar:
curl -fsSL https://raw.githubusercontent.com/SEU-REPO/SunOps---SaaS/main/scripts/deploy-ec2-full.sh -o deploy.sh
chmod +x deploy.sh
sudo ./deploy.sh
```

## 5️⃣ Verificar
```bash
# Status
sudo docker-compose -f /opt/crm-solar/docker-compose.yml ps

# Logs
sudo docker-compose -f /opt/crm-solar/docker-compose.yml logs -f

# Health check
curl http://localhost/health/
```

---

## ⚡ COMANDO ÚNICO (copie e cole)
```bash
export AWS_ACCESS_KEY_ID=SUA-ACCESS-KEY
export AWS_SECRET_ACCESS_KEY=SUA-SECRET-KEY
export AWS_REGION=us-east-1
export INSTANCE_ID=i-07a9e55abd9e8a7be

# Obter IP
EC2_IP=$(aws ec2 describe-instances --instance-ids $INSTANCE_ID --query 'Reservations[0].Instances[0].PublicIpAddress' --output text)
echo "IP: $EC2_IP"

# Configurar Security Group
SG_ID=$(aws ec2 describe-instances --instance-ids $INSTANCE_ID --query 'Reservations[0].Instances[0].SecurityGroups[0].GroupId' --output text)
aws ec2 authorize-security-group-ingress --group-id $SG_ID --protocol tcp --port 80 --cidr 0.0.0.0/0 2>/dev/null || true
aws ec2 authorize-security-group-ingress --group-id $SG_ID --protocol tcp --port 443 --cidr 0.0.0.0/0 2>/dev/null || true

echo "✅ Security Group configurado"
echo "🌐 Acesse: http://$EC2_IP"
echo ""
echo "📝 Agora conecte via SSH e execute o deploy:"
echo "ssh -i sua-chave.pem ubuntu@$EC2_IP"
```
