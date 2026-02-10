# ⚡ DEPLOY AWS COM TERRAFORM (5 MIN)

## 📋 O QUE VOCÊ PRECISA ME PASSAR:

1. **AWS Credentials:**
   ```bash
   AWS_ACCESS_KEY_ID=AKIA...
   AWS_SECRET_ACCESS_KEY=...
   ```

2. **SSH Key Name** (nome da chave que já existe na AWS)
   ```
   Exemplo: minha-chave-aws
   ```

3. **Senha do RDS** (mínimo 8 caracteres)
   ```
   Exemplo: SenhaForte@123
   ```

4. **GitHub Repo URL** (se privado, precisa de token)
   ```
   https://github.com/SEU-USUARIO/SunOps---SaaS.git
   ```

## 🚀 COMANDOS PARA EXECUTAR:

```bash
cd terraform

# Configurar AWS
export AWS_ACCESS_KEY_ID="sua-access-key"
export AWS_SECRET_ACCESS_KEY="sua-secret-key"

# Inicializar Terraform
terraform init

# Criar arquivo de variáveis
cat > terraform.tfvars << EOF
aws_region    = "us-east-1"
environment   = "dev"
ssh_key_name  = "SUA-CHAVE-SSH"
db_password   = "SUA-SENHA-RDS"
EOF

# Planejar
terraform plan -var-file=terraform.tfvars

# Aplicar (criar infraestrutura)
terraform apply -var-file=terraform.tfvars -auto-approve
```

## ⏱️ TEMPO ESTIMADO:
- RDS: ~5 min
- EC2 Spot: ~2 min
- Deploy automático: ~3 min
- **Total: ~10 min**

## 📊 OUTPUTS:
Após o deploy, você receberá:
```
ec2_public_ip = "54.123.45.67"
rds_endpoint  = "crm-solar-db-dev.xxx.rds.amazonaws.com:5432"
app_url       = "http://54.123.45.67"
```

## ✅ ACESSAR:
```
Frontend: http://SEU-IP
Admin: http://SEU-IP/admin
User: admin
Pass: Admin@123456
```

## 🗑️ DESTRUIR TUDO:
```bash
terraform destroy -var-file=terraform.tfvars -auto-approve
```

## 💰 CUSTO ESTIMADO:
- EC2 Spot t3.medium: ~$15/mês
- RDS db.t3.micro: ~$15/mês
- EIP: ~$3/mês
- **Total: ~$33/mês**

## 🔧 TROUBLESHOOTING:

### Erro de chave SSH
```bash
# Criar nova chave na AWS
aws ec2 create-key-pair --key-name crm-solar-key --query 'KeyMaterial' --output text > crm-solar-key.pem
chmod 400 crm-solar-key.pem
```

### Ver logs do deploy
```bash
# SSH na instância
ssh -i sua-chave.pem ubuntu@SEU-IP
sudo tail -f /var/log/user-data.log
```

### Verificar status
```bash
ssh -i sua-chave.pem ubuntu@SEU-IP
sudo docker-compose -f /opt/crm-solar/docker-compose.dev.yml ps
```
