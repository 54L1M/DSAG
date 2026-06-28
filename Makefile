# DSAG — DSA Gym.

# Filter to one topic with k=<name>, e.g.  make test k=binary_search
# Pass extra args with ARGS=..., e.g.       make bench ARGS="--sizes 1000 5000"

.DEFAULT_GOAL := help

# `make test k=binary_search` -> pytest -k binary_search
ifdef k
PYTEST_K := -k $(k)
endif

.PHONY: help setup test test-solutions lint fmt check drill topics target bench clean

help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) \
		| sort \
		| awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-16s\033[0m %s\n", $$1, $$2}'

setup: ## Create the venv and install dev deps (pytest, ruff)
	uv sync

test: ## Run the suite against your code (k=<name> to filter)
	uv run pytest $(PYTEST_K) $(ARGS)

test-solutions: ## Run the suite against the reference solutions (should be all green)
	ALGO_TARGET=solutions uv run pytest $(PYTEST_K) $(ARGS)

lint: ## Lint with ruff
	uv run ruff check $(ARGS)

fmt: ## Format with ruff
	uv run ruff format $(ARGS)

check: lint test ## Lint, then run the suite

drill: ## Fresh blank stubs in a new src/days/dayN and point the target at it
	uv run python drill.py $(ARGS)

topics: ## Point the test target back at the src/topics study workspace
	uv run python drill.py --topics

target: ## Show the active test target
	uv run python drill.py --show

bench: ## Race the sorts (ARGS="--solutions --sizes 1000 5000")
	uv run python bench.py $(ARGS)

clean: ## Remove caches and drill scratch (src/days)
	rm -rf .pytest_cache .ruff_cache src/days
	find . -type d -name __pycache__ -not -path './.venv/*' -exec rm -rf {} +
