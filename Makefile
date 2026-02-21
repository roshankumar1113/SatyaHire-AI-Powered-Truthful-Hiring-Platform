# AI Interview Platform - Makefile

.PHONY: help dev-up dev-down build test lint clean

# Default target
help:
	@echo "AI Interview Platform - Available Commands"
	@echo ""
	@echo "Development:"
	@echo "  make dev-up          - Start all services in development mode"
	@echo "  make dev-down        - Stop all services"
	@echo "  make logs            - View logs from all services"
	@echo ""
	@echo "Database:"
	@echo "  make migrate-up      - Run database migrations"
	@echo "  make migrate-down    - Rollback database migrations"
	@echo "  make seed            - Seed database with sample data"
	@echo ""
	@echo "Testing:"
	@echo "  make test            - Run all tests"
	@echo "  make test-unit       - Run unit tests"
	@echo "  make test-integration - Run integration tests"
	@echo "  make test-load       - Run load tests"
	@echo ""
	@echo "Code Quality:"
	@echo "  make lint            - Run linters"
	@echo "  make format          - Format code"
	@echo "  make security-scan   - Run security scan"
	@echo ""
	@echo "Build:"
	@echo "  make build           - Build all services"
	@echo "  make docker-build    - Build Docker images"
	@echo "  make docker-push     - Push Docker images"
	@echo ""
	@echo "Deployment:"
	@echo "  make deploy-staging  - Deploy to staging"
	@echo "  make deploy-prod     - Deploy to production"
	@echo ""

# Development
dev-up:
	@echo "Starting development environment..."
	docker-compose up -d
	@echo "Services started! Access:"
	@echo "  - Frontend: http://localhost:3000"
	@echo "  - Backend: http://localhost:8000"
	@echo "  - API Docs: http://localhost:8000/api/docs"

dev-down:
	@echo "Stopping development environment..."
	docker-compose down

logs:
	docker-compose logs -f

# Database
migrate-up:
	@echo "Running database migrations..."
	cd skillproof-backend && python -m alembic upgrade head

migrate-down:
	@echo "Rolling back database migrations..."
	cd skillproof-backend && python -m alembic downgrade -1

seed:
	@echo "Seeding database..."
	cd skillproof-backend && python scripts/seed_db.py

# Testing
test: test-unit test-integration
	@echo "All tests completed!"

test-unit:
	@echo "Running unit tests..."
	cd skillproof-backend && pytest tests/unit -v --cov=app

test-integration:
	@echo "Running integration tests..."
	cd skillproof-backend && pytest tests/integration -v

test-load:
	@echo "Running load tests..."
	cd tests/load && k6 run load_test.js

# Code Quality
lint:
	@echo "Running linters..."
	cd skillproof-backend && flake8 app/
	cd skillproof-backend && black --check app/
	cd skillproof-backend && mypy app/

format:
	@echo "Formatting code..."
	cd skillproof-backend && black app/
	cd skillproof-backend && isort app/

security-scan:
	@echo "Running security scan..."
	docker run --rm -v $(PWD):/src aquasec/trivy fs /src

# Build
build:
	@echo "Building services..."
	cd skillproof-backend && pip install -r requirements.txt
	cd skillproof-frontend && npm install

docker-build:
	@echo "Building Docker images..."
	docker-compose build

docker-push:
	@echo "Pushing Docker images..."
	docker-compose push

# Deployment
deploy-staging:
	@echo "Deploying to staging..."
	kubectl apply -f infrastructure/kubernetes/ --namespace=ai-interview-staging

deploy-prod:
	@echo "Deploying to production..."
	kubectl apply -f infrastructure/kubernetes/ --namespace=ai-interview-prod

# Cleanup
clean:
	@echo "Cleaning up..."
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name "node_modules" -exec rm -rf {} +
