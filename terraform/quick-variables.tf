variable "aws_region" {
  description = "AWS Region"
  type        = string
  default     = "us-east-1"
}

variable "project_name" {
  description = "Nome do projeto"
  type        = string
  default     = "crm-solar"
}

variable "environment" {
  description = "Ambiente (dev ou prod)"
  type        = string
  default     = "dev"
}

variable "db_password" {
  description = "Senha do RDS PostgreSQL"
  type        = string
  sensitive   = true
}

variable "ssh_key_name" {
  description = "Nome da chave SSH na AWS"
  type        = string
}
