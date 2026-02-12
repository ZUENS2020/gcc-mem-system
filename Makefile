.PHONY: help build test test-docker up down logs

help:
	@echo "Available targets:"
	@echo "  make build       - Build Docker image"
	@echo "  make up          - Start GCC server"
	@echo "  make down        - Stop services"
	@echo "  make logs        - Show service logs"
	@echo "  make test        - Run tests locally"
	@echo "  make test-docker - Run tests in Docker"
	@echo "  make shell       - Open shell in container"

build:
	docker build -t gcc-system:latest .

up:
	docker-compose up -d gcc-mcp

down:
	docker-compose down

logs:
	docker-compose logs -f gcc-mcp

test:
	python -m pytest tests/ -v

test-docker:
	docker-compose run --rm gcc-test

shell:
	docker-compose run --rm gcc-mcp bash

# Install dependencies locally
install:
	pip install -e .

# Run server locally
run:
	python -m gcc.server.app
