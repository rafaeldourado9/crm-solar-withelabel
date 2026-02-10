output "ec2_public_ip" {
  description = "IP público da instância EC2"
  value       = aws_eip.app.public_ip
}

output "rds_endpoint" {
  description = "Endpoint do RDS"
  value       = aws_db_instance.postgres.endpoint
}

output "s3_bucket_storage" {
  description = "Nome do bucket S3 de storage"
  value       = aws_s3_bucket.storage.id
}

output "s3_bucket_backups" {
  description = "Nome do bucket S3 de backups"
  value       = aws_s3_bucket.backups.id
}

output "database_url" {
  description = "URL de conexão do banco"
  value       = "postgresql://${aws_db_instance.postgres.username}:${var.db_password}@${aws_db_instance.postgres.endpoint}/${aws_db_instance.postgres.db_name}"
  sensitive   = true
}
