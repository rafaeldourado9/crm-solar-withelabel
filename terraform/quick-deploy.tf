terraform {
  required_version = ">= 1.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

# VPC e Subnet padrão
data "aws_vpc" "default" {
  default = true
}

data "aws_subnets" "default" {
  filter {
    name   = "vpc-id"
    values = [data.aws_vpc.default.id]
  }
}

# Security Group EC2
resource "aws_security_group" "ec2" {
  name        = "${var.project_name}-ec2-${var.environment}"
  description = "Security group for EC2"
  vpc_id      = data.aws_vpc.default.id

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# Security Group RDS
resource "aws_security_group" "rds" {
  name        = "${var.project_name}-rds-${var.environment}"
  description = "Security group for RDS"
  vpc_id      = data.aws_vpc.default.id

  ingress {
    from_port       = 5432
    to_port         = 5432
    protocol        = "tcp"
    security_groups = [aws_security_group.ec2.id]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# RDS PostgreSQL
resource "aws_db_instance" "postgres" {
  identifier             = "${var.project_name}-db-${var.environment}"
  engine                 = "postgres"
  engine_version         = "15.4"
  instance_class         = "db.t3.micro"
  allocated_storage      = 20
  storage_type           = "gp2"
  db_name                = "crm_solar_${var.environment}"
  username               = "postgres"
  password               = var.db_password
  vpc_security_group_ids = [aws_security_group.rds.id]
  publicly_accessible    = false
  skip_final_snapshot    = true
  backup_retention_period = 7
}

# EC2 Spot Instance
resource "aws_spot_instance_request" "app" {
  ami                    = "ami-0c7217cdde317cfec" # Ubuntu 22.04 us-east-1
  instance_type          = "t3.medium"
  key_name               = var.ssh_key_name
  vpc_security_group_ids = [aws_security_group.ec2.id]
  
  spot_price    = "0.05"
  spot_type     = "persistent"
  wait_for_fulfillment = true

  user_data = templatefile("${path.module}/user_data.sh", {
    db_host     = aws_db_instance.postgres.address
    db_password = var.db_password
    environment = var.environment
  })

  tags = {
    Name        = "${var.project_name}-app-${var.environment}"
    Environment = var.environment
  }
}

# Elastic IP
resource "aws_eip" "app" {
  instance = aws_spot_instance_request.app.spot_instance_id
  domain   = "vpc"
}

# Outputs
output "ec2_public_ip" {
  value = aws_eip.app.public_ip
}

output "rds_endpoint" {
  value = aws_db_instance.postgres.endpoint
}

output "app_url" {
  value = "http://${aws_eip.app.public_ip}"
}
