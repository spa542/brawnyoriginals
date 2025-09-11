.PHONY: install dev build test clean help

# Default target
all: help

# Help target to show all available commands
help:
	@echo "Frontend commands:"
	@echo "  make install     - Install Node.js dependencies"
	@echo "  make dev         - Start the development server"
	@echo "  make build       - Build for production"
	@echo "  make preview     - Preview the production build"
	@echo "  make test        - Run tests"
	@echo "  make clean       - Clean build artifacts"
	@echo "  make format      - Format code with Prettier"
	@echo "  make lint        - Lint code with ESLint"
	@echo "  make type-check  - Run TypeScript type checking"

# Install Node.js dependencies
install:
	@echo "Installing Node.js dependencies..."
	npm install

# Start the development server
dev:
	@echo "Starting Vite development server..."
	npm run dev

# Build for production
build:
	@echo "Building for production..."
	npm run build

# Preview the production build
preview:
	@echo "Previewing production build..."
	npm run preview

# Run tests
test:
	@echo "Running tests..."
	npm run test

# Clean build artifacts
clean:
	@echo "Cleaning build artifacts..."
	rm -rf node_modules
	rm -rf dist
	rm -rf .next
	rm -rf .turbo
	rm -f package-lock.json
	rm -f pnpm-lock.yaml
	rm -f yarn.lock

# Format code
format:
	@echo "Formatting code with Prettier..."
	npx prettier --write .

# Lint code
lint:
	@echo "Linting code with ESLint..."
	npm run lint

# Type check
type-check:
	@echo "Running TypeScript type checking..."
	npm run type-check

%:
	@:
