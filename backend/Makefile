.PHONY: venv install dev build test clean help format lint

# Virtual environment directory
VENV = venv
PYTHON = $(VENV)/bin/python3
PIP = $(VENV)/bin/pip
UVICORN = $(VENV)/bin/uvicorn

# Default target
all: help

# Help target to show all available commands
help:
	@echo "Backend commands:"
	@echo "  make venv        - Create a Python virtual environment"
	@echo "  make install     - Install Python dependencies"
	@echo "  make dev         - Start the development server"
	@echo "  make build       - Build for production"
	@echo "  make serve       - Start production server (requires built frontend)"
	@echo "  make test        - Run tests"
	@echo "  make clean       - Clean build artifacts and virtual environment"
	@echo "  make format      - Format code with Black and isort"
	@echo "  make lint        - Lint code with flake8"

# Create and activate virtual environment
venv:
	@echo "Creating Python virtual environment..."
	python3 -m venv $(VENV)
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt

# Install Python dependencies
install: venv
	@echo "Installing/updating Python dependencies..."
	$(PIP) install --upgrade -r requirements.txt

# Start the development server
dev: install
	@echo "Starting FastAPI development server..."
	PYTHONPATH=. $(UVICORN) app.main:app --reload --host 0.0.0.0 --port 8000

# Build for production
build: install
	@echo "Building for production..."
	$(PIP) install --upgrade -r requirements.txt --no-cache-dir

# Start production server
serve: build
	@echo "Starting production server..."
	@if [ ! -d "../frontend/dist" ]; then \
		echo "Error: Frontend not built. Run 'make build' in the frontend directory first."; \
		exit 1; \
	fi
	export ENV=production && \
	$(PYTHON) -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4

# Run tests
test: install
	@echo "Running tests..."
	# Add your test command here
	# Example: $(PYTHON) -m pytest

# Clean build artifacts and virtual environment
clean:
	@echo "Cleaning Python environment..."
	@if [ -d "$(VENV)" ]; then \
		echo "Removing virtual environment..."; \
		rm -rf $(VENV); \
	fi
	@echo "Removing Python cache files..."
	@find . -type d -name "__pycache__" -exec rm -r {} + 2>/dev/null || true
	@find . -type f -name "*.pyc" -delete 2>/dev/null || true
	@find . -type f -name "*.pyo" -delete 2>/dev/null || true
	@find . -type d -name ".pytest_cache" -exec rm -r {} + 2>/dev/null || true
	@find . -type d -name ".mypy_cache" -exec rm -r {} + 2>/dev/null || true

# Format code
format: venv
	@echo "Formatting code with Black and isort..."
	$(VENV)/bin/black .
	$(VENV)/bin/isort .

# Lint code
lint: venv
	@echo "Linting code with flake8..."
	$(VENV)/bin/flake8 .

%:
	@:
