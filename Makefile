.PHONY: all install dev build test clean help

# Default target
all: help

# Help target to show all available commands
help:
	@echo "Available commands:"
	@echo "  make install     - Install all dependencies (frontend and backend)"
	@echo "  make dev         - Start both frontend and backend in development mode"
	@echo "  make build       - Build both frontend and backend for production"
	@echo "  make serve       - Start production server (serves both frontend and backend on port 8000)"
	@echo "  make test        - Run tests for both frontend and backend"
	@echo "  make clean       - Clean build artifacts"
	@echo "  make frontend    - Run frontend-specific commands (e.g., 'make frontend install')"
	@echo "  make backend     - Run backend-specific commands (e.g., 'make backend install')"

# Install all dependencies
install:
	@echo "Installing all dependencies..."
	@$(MAKE) -C backend install
	@$(MAKE) -C frontend install

# Start development servers
dev:
	@echo "Starting development servers..."
	@$(MAKE) -C backend dev &\
	$(MAKE) -C frontend dev

# Start production server (serves both frontend and backend)
serve:
	@echo "Building frontend for production..."
	@$(MAKE) -C frontend build
	@echo "\nStarting production server..."
	@echo "Access the application at http://localhost:8000"
	@echo "API documentation at http://localhost:8000/api/docs\n"
	@$(MAKE) -C backend serve

# Build for production
build:
	@echo "Building for production..."
	@$(MAKE) -C backend build
	@$(MAKE) -C frontend build

# Run tests
test:
	@echo "Running tests..."
	@$(MAKE) -C backend test
	@$(MAKE) -C frontend test

# Clean build artifacts
clean:
	@echo "Cleaning..."
	@$(MAKE) -C backend clean
	@$(MAKE) -C frontend clean

# Frontend-specific commands
frontend:
	@$(MAKE) -C frontend $(filter-out $@,$(MAKECMDGOALS))

# Backend-specific commands
backend:
	@$(MAKE) -C backend $(filter-out $@,$(MAKECMDGOALS))

# Server deployment target (assumes frontend dist is already built)
deploy:
	@echo "Preparing for server deployment..."
	export ENV=production
	@if [ ! -d "frontend/dist" ]; then \
		echo "Error: frontend/dist directory not found. Please build the frontend first."; \
		exit 1; \
	fi
	@echo "Building backend for production..."
	@$(MAKE) -C backend build
	@echo "\nDeployment ready! The application can be served using the backend production server."

# Handle targets with colons (e.g., make backend:install)
%:
	@:
