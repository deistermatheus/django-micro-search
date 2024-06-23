# Makefile for running Black and Ruff

# Define Poetry commands
POETRY_RUN = poetry run

# Define targets
.PHONY: lint
lint:
	@$(POETRY_RUN) ruff check . --fix

.PHONY: format
format:
	@$(POETRY_RUN) ruff format .

.PHONY: typing
typing:
	@$(POETRY_RUN) mypy --explicit-package-bases ./app

.PHONY: containers
containers:
	@docker-compose up -d

.PHONY: check
check: lint format typing
	@echo "Linting, formatting and static type check completed."