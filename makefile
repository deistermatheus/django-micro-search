# Makefile for running Black and Ruff

# Define Poetry commands
POETRY_RUN = poetry run

# Define targets
.PHONY: lint
lint:
	@$(POETRY_RUN) ruff check app

.PHONY: format
format:
	@$(POETRY_RUN) black app

.PHONY: check
check: lint format
	@echo "Linting and formatting check completed."