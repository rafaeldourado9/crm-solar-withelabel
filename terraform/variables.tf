variable "aws_region" {
  description = "AWS Region"
  type        = string
  default     = "us-east-1"
}

variable "project_name" {
  description = "Nome do projeto"
  type        = string
  default     = "sunops"
}

variable "environment" {
  description = "Ambiente (dev ou prod)"
  type        = string
}

variable "db_password" {
  description = "Senha do banco de dados"
  type        = string
  sensitive   = true
}

variable "ssh_key_name" {
  description = "Nome da chave SSH"
  type        = string
  default     = "sunops-key"
}

variable "domain_name" {
  description = "Domínio principal"
  type        = string
  default     = "sunops.com.br"
}
