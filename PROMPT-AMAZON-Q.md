# PROMPT PARA AMAZON Q - DEPLOY AWS

Cole este prompt no Amazon Q Developer:

---

Preciso fazer deploy de uma aplicação Django + React + PostgreSQL na AWS usando Terraform. 

**Requisitos:**

1. **RDS PostgreSQL:**
   - Engine: PostgreSQL 15.4
   - Instance: db.t3.micro
   - Storage: 20GB gp2
   - Backup: 7 dias
   - Database name: crm_solar_dev
   - Username: postgres
   - Password: [variável sensível]
   - Publicly accessible: false

2. **EC2 Spot Instance:**
   - AMI: Ubuntu 22.04 LTS (us-east-1: ami-0c7217cdde317cfec)
   - Instance type: t3.medium
   - Spot price: $0.05
   - Spot type: persistent
   - User data: instalar Docker, Docker Compose, clonar repo, fazer deploy

3. **Security Groups:**
   - EC2: portas 22, 80, 443 (entrada), all (saída)
   - RDS: porta 5432 apenas do EC2 (entrada)

4. **Elastic IP:**
   - Associar ao EC2 Spot

5. **User Data Script deve:**
   - Instalar Docker e Docker Compose
   - Clonar repo: https://github.com/SEU-USUARIO/SunOps---SaaS.git (branch dev)
   - Criar arquivo .env.dev com:
     * SECRET_KEY (gerar com openssl)
     * DEBUG=False
     * ALLOWED_HOSTS=*
     * DB_HOST=${rds_endpoint}
     * DB_PASSWORD=${var.db_password}
     * REDIS_HOST=localhost
   - Executar: docker-compose -f docker-compose.dev.yml up -d --build
   - Executar migrações: python manage.py migrate
   - Verificar equipamentos: python verificar_equipamentos.py
   - Criar superuser: admin/Admin@123456
   - Configurar monitoramento automático (systemd service)

6. **Outputs necessários:**
   - ec2_public_ip
   - rds_endpoint
   - app_url

7. **Variáveis:**
   - aws_region (default: us-east-1)
   - environment (default: dev)
   - project_name (default: crm-solar)
   - db_password (sensitive)
   - ssh_key_name

**Estrutura de arquivos:**
- main.tf (provider, resources)
- variables.tf (variáveis)
- outputs.tf (outputs)
- user_data.sh (script de inicialização)
- terraform.tfvars.example (exemplo de valores)

**Importante:**
- Usar VPC e subnets default
- RDS deve estar na mesma VPC do EC2
- EC2 deve ter acesso à internet para instalar pacotes
- Logs do user_data em /var/log/user-data.log
- Deploy deve ser totalmente automatizado

Gere os arquivos Terraform completos e funcionais.

---

**Depois de gerar, me passe:**
1. AWS_ACCESS_KEY_ID
2. AWS_SECRET_ACCESS_KEY
3. Nome da chave SSH (ou crie uma nova)
4. Senha para o RDS (mínimo 8 caracteres)
5. URL do repositório GitHub (se privado, token também)
