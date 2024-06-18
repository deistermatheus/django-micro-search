# Makefile for running Black and Ruff

# Define Poetry commands
POETRY_RUN = poetry run

# Define targets
.PHONY: lint
lint:
	@$(POETRY_RUN) ruff check app --fix

.PHONY: format
format:
	@$(POETRY_RUN) ruff format app --fix

.PHONY: typing
format:
	@$(POETRY_RUN) mypy app

.PHONY: containers
format:
	@docker-compose up -d

.PHONY: check
check: lint format typing
	@echo "Linting, formatting and static type check completed."