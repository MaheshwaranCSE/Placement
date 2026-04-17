.PHONY: up down logs migrate seed migrate_json backup test lint shell superuser

up:
	docker-compose up -d --build

down:
	docker-compose down

logs:
	docker-compose logs -f web celery_worker

migrate:
	docker-compose exec web flask db upgrade

seed:
	docker-compose exec web python scripts/seed_data.py

migrate_json:
	docker-compose exec web python scripts/migrate_json.py

backup:
	docker-compose exec postgres /backup/backup_db.sh

test:
	docker-compose run --rm web pytest --cov=backend

lint:
	docker-compose run --rm web bandit -r backend/

shell:
	docker-compose exec web flask shell

superuser:
	docker-compose exec web python -c "from scripts.seed_data import create_admin; create_admin()"
