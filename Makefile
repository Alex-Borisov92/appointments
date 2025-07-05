# ------------------------------------------------------------------------------
# VARIABLES
# ------------------------------------------------------------------------------
COMPOSE ?= docker compose
PY      ?= poetry run python
ENVFILE ?= .env

# ------------------------------------------------------------------------------
# QUALITY
# ------------------------------------------------------------------------------
lint:
	flake8 . && isort --check . && black --check .

format:
	isort . && black .

typecheck:  # mypy ≥90 %
	mypy . --strict --ignore-missing-imports --txt-report mypy_report
	@tail -1 mypy_report/index.txt

test:
	pytest -q

ci: lint typecheck test  # единая команда для локальной проверки

# ------------------------------------------------------------------------------
# DOCKER
# ------------------------------------------------------------------------------
up:  ## build + run (detached)
	$(COMPOSE) up -d --build

down:  ## stop and remove containers
	$(COMPOSE) down

restart: down up  ## easy reboot

logs:  ## tail -f
	$(COMPOSE) logs -f --tail=100

# ------------------------------------------------------------------------------
# MIGRATIONS (alembic stub)
# ------------------------------------------------------------------------------
migrate:
	@echo "Running alembic upgrade head (placeholder)…"
	$(COMPOSE) exec api alembic upgrade head

migrate-revision:
	@read -p "Message: " msg && \
	$(COMPOSE) exec api alembic revision --autogenerate -m "$$msg"

# ------------------------------------------------------------------------------
# DATABASE CONVENIENCE
# ------------------------------------------------------------------------------
psql:
	$(COMPOSE) exec db psql -U $$POSTGRES_USER $$POSTGRES_DB

dropdb:
	@echo "!!! DANGER: dropping the database !!!"
	$(COMPOSE) exec db dropdb -U $$POSTGRES_USER $$POSTGRES_DB || true
	$(COMPOSE) exec db createdb -U $$POSTGRES_USER $$POSTGRES_DB

# ------------------------------------------------------------------------------
# HELP
# ------------------------------------------------------------------------------
.PHONY: help
help:  ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?##' $(MAKEFILE_LIST) | \
		awk 'BEGIN {FS = ":.*?##"}; {printf "\033[36m%-16s\033[0m %s\n", $$1, $$2}'
