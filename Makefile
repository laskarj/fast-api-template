IMAGE_NAME=web-app
HOST=0.0.0.0
PORT=8000
DOCKER=docker compose -f $(or $(DOCKER_COMPOSE_FILE), docker-compose.yaml)
EXEC=$(DOCKER) exec $(or $(c), $(IMAGE_NAME))

lint: ## Run linter
	ruff format
	ruff check --fix

lint-no-format: ## Run linter without formatting
	ruff check

app:  ## Run app
	python -m app

build: ## Build all or c=<name> containers in foreground
	$(DOCKER) up --build $(c)

build-d: ## Build all or c=<name> containers in background
	$(DOCKER) up --build -d $(c)

stop: ## Stop all or c=<name> containers
	$(DOCKER) stop $(c)

restart: ## Restart all or c=<name> containers
	$(DOCKER) restart $(c)

rebuild: ## Rebuild all or c=<name> containers
	$(DOCKER) down
	$(DOCKER) up --build -d $(c)

logs: ## Show logs for all or c=<name> containers
	$(DOCKER) logs --tail=$(or $(n), 100) -f $(c)

status: ## Show status of containers
	$(DOCKER) ps

images: ## Show all images
	$(DOCKER) images

prune:  ## Drop all docker images, containers, volumes
	docker stop $(shell docker ps -qa) && docker system prune -af --volumes

exec: ## Exec container
	$(EXEC) sh

alembic-head:  ## Apply migrations
	python -Om alembic upgrade head

pre-commit-setup:  ## Setup pre-commit hook
	pre-commit --version
	pre-commit install
	pre-commit run --all-files
