# Sistema de Fallback - CRM Solar

## 🛡️ Componentes

### 1. Database Fallback Middleware
- Detecta falhas de conexão com banco
- Retorna resposta HTTP 503 com mensagem amigável
- Evita crashes da aplicação

### 2. Health Check Endpoint
- **URL:** `/health/`
- **Verifica:**
  - Conexão com PostgreSQL
  - Conexão com Redis
- **Retorna:**
  - 200 OK se tudo funcionando
  - 503 Service Unavailable se houver problemas

### 3. Monitor Automático
- Verifica health check a cada 30 segundos
- Após 3 falhas consecutivas, reinicia o backend
- Logs em `/var/log/crm-solar-monitor.log`

### 4. Connection Pooling
- `CONN_MAX_AGE`: 60 segundos
- `connect_timeout`: 10 segundos
- Reutiliza conexões para melhor performance

## 🚀 Instalação

```bash
# Já incluído no deploy automático
sudo cp scripts/crm-solar-monitor.service /etc/systemd/system/
sudo systemctl enable crm-solar-monitor
sudo systemctl start crm-solar-monitor
```

## 📊 Monitoramento

```bash
# Status do monitor
sudo systemctl status crm-solar-monitor

# Logs em tempo real
sudo journalctl -u crm-solar-monitor -f

# Logs do arquivo
tail -f /var/log/crm-solar-monitor.log

# Health check manual
curl http://localhost/health/
```

## 🔄 Fluxo de Recuperação

1. Monitor detecta falha (HTTP != 200)
2. Incrementa contador de falhas
3. Após 3 falhas consecutivas:
   - Reinicia container backend
   - Aguarda 10 segundos
   - Reseta contador
4. Sistema volta ao normal

## ⚙️ Configurações

### Ajustar sensibilidade
Editar `/opt/crm-solar/scripts/monitor.sh`:
```bash
MAX_FAILURES=3      # Número de falhas antes de reiniciar
sleep 30            # Intervalo entre checks (segundos)
```

### Desabilitar monitor
```bash
sudo systemctl stop crm-solar-monitor
sudo systemctl disable crm-solar-monitor
```

## 🆘 Troubleshooting

### Monitor não inicia
```bash
# Verificar permissões
sudo chmod +x /opt/crm-solar/scripts/monitor.sh

# Verificar logs
sudo journalctl -u crm-solar-monitor -n 50
```

### Muitos restarts
```bash
# Verificar logs do backend
sudo docker-compose -f docker-compose.dev.yml logs backend

# Verificar conexão RDS
sudo docker-compose -f docker-compose.dev.yml exec backend python manage.py dbshell
```

## 📈 Métricas

O sistema registra:
- Timestamp de cada check
- Status HTTP retornado
- Número de falhas consecutivas
- Ações de restart executadas
