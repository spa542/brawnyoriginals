# Backend Makefile Documentation

This document describes the available make targets for the FastAPI backend.

## Virtual Environment Management

### `make venv`
Creates a Python virtual environment in the `venv` directory and installs all required dependencies.

### `make install`
Ensures the virtual environment exists and installs/updates all Python dependencies from `requirements.txt`.

## Development

### `make dev`
Starts the FastAPI development server with auto-reload enabled.
- **Access API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Alternative Docs**: http://localhost:8000/redoc

## Code Quality

### `make format`
Formats Python code using:
- Black for code formatting
- isort for import sorting

### `make lint`
Runs flake8 to check for code style and potential issues.

## Testing

### `make test`
Runs the test suite. Add your test commands here as needed.

## Production

### `make build`
Prepares the application for production by installing dependencies with `--no-cache-dir`.

## Cleanup

### `make clean`
Removes:
- The virtual environment directory
- Python cache files (`__pycache__`, `*.pyc`, `*.pyo`)
- Test and type checking caches (`.pytest_cache/`, `.mypy_cache/`)

## Environment Variables

The following environment variables are used by the Makefile:
- `VENV`: Virtual environment directory (default: `venv`)
- `PYTHON`: Path to the Python interpreter in the virtual environment
- `PIP`: Path to pip in the virtual environment
- `UVICORN`: Path to uvicorn in the virtual environment

## Usage Example

```bash
# First time setup
make install

# Start development server
make dev

# Format and check code
make format
make lint

# Clean up
make clean
```
