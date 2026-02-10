$env:AWS_ACCESS_KEY_ID="SUA-ACCESS-KEY-AQUI"
$env:AWS_SECRET_ACCESS_KEY="SUA-SECRET-KEY-AQUI"
$env:AWS_REGION="us-east-1"
$INSTANCE_ID="i-07a9e55abd9e8a7be"

Write-Host "Obtendo informacoes do EC2..." -ForegroundColor Cyan

# Obter IP
$EC2_IP = aws ec2 describe-instances `
  --instance-ids $INSTANCE_ID `
  --query 'Reservations[0].Instances[0].PublicIpAddress' `
  --output text

Write-Host "IP Publico: $EC2_IP" -ForegroundColor Green

# Obter Security Group
$SG_ID = aws ec2 describe-instances `
  --instance-ids $INSTANCE_ID `
  --query 'Reservations[0].Instances[0].SecurityGroups[0].GroupId' `
  --output text

Write-Host "Security Group: $SG_ID" -ForegroundColor Green

# Configurar portas
Write-Host "`nConfigurando Security Group..." -ForegroundColor Cyan

aws ec2 authorize-security-group-ingress `
  --group-id $SG_ID `
  --protocol tcp `
  --port 80 `
  --cidr 0.0.0.0/0 2>$null

aws ec2 authorize-security-group-ingress `
  --group-id $SG_ID `
  --protocol tcp `
  --port 443 `
  --cidr 0.0.0.0/0 2>$null

Write-Host "Security Group configurado!" -ForegroundColor Green

Write-Host "`n============================================" -ForegroundColor Yellow
Write-Host "PROXIMOS PASSOS:" -ForegroundColor Yellow
Write-Host "============================================" -ForegroundColor Yellow
Write-Host ""
Write-Host "1. Conecte via SSH:" -ForegroundColor Cyan
Write-Host "   ssh -i sua-chave.pem ubuntu@$EC2_IP" -ForegroundColor White
Write-Host ""
Write-Host "2. Execute no EC2:" -ForegroundColor Cyan
Write-Host "   curl -fsSL https://raw.githubusercontent.com/SEU-REPO/SunOps---SaaS/main/scripts/deploy-ec2-full.sh -o deploy.sh" -ForegroundColor White
Write-Host "   chmod +x deploy.sh" -ForegroundColor White
Write-Host "   sudo ./deploy.sh" -ForegroundColor White
Write-Host ""
Write-Host "3. Acesse:" -ForegroundColor Cyan
Write-Host "   http://$EC2_IP" -ForegroundColor White
Write-Host "   http://$EC2_IP/admin" -ForegroundColor White
Write-Host ""
Write-Host "Credenciais:" -ForegroundColor Cyan
Write-Host "   User: admin" -ForegroundColor White
Write-Host "   Pass: Admin@123456" -ForegroundColor White
Write-Host ""
