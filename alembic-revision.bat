@echo off
docker-compose exec backend python -m alembic revision -m "%*"
