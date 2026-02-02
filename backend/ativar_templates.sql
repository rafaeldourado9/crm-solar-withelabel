-- Script para ativar todos os templates
-- Execute este script no PostgreSQL ou via Docker:
-- docker-compose exec db psql -U postgres -d crm_solar -f /path/to/this/file.sql

UPDATE templates SET ativo = true WHERE ativo = false OR ativo IS NULL;

-- Verificar resultado
SELECT id, nome, tipo, ativo FROM templates;
