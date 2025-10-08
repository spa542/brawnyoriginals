# Makefile Documentation

This project uses a hierarchical Makefile structure to manage the development workflow. The following documentation explains the available make targets and their purposes.

## Root Makefile

Located at the project root, this Makefile provides high-level commands to manage both frontend and backend services.

### Available Commands:

- `make install` - Install all dependencies (frontend and backend)
- `make dev` - Start both frontend and backend in development mode
- `make build` - Build both frontend and backend for production
- `make deploy` - Prepare for server deployment (requires frontend/dist to exist)
- `make test` - Run tests for both frontend and backend
- `make clean` - Clean build artifacts
- `make frontend [target]` - Run frontend-specific commands (e.g., `make frontend lint`)
- `make backend [target]` - Run backend-specific commands (e.g., `make backend test`)

## Deployment

For server deployment, follow these steps:

1. First, build the frontend:
   ```bash
   make -C frontend build
   ```

2. **Important**: Commit and push the built frontend files to your repository:
   ```bash
   git add frontend/dist
   git commit -m "build: update frontend production build"
   git push
   ```

3. On your server, pull the latest changes and run the deployment target:
   ```bash
   git pull
   make deploy
   ```

This will:
- Verify the frontend/dist directory exists
- Build the backend for production
- Prepare the application for serving

The application can then be served using the backend production server.

> **Note**: The frontend's `dist` directory must be committed to the repository as it contains the production-ready static files that will be served by the backend.

## Backend Makefile

Located in the `backend/` directory, this Makefile manages the Python FastAPI backend.

### Available Commands:

- `make venv` - Create a Python virtual environment
- `make install` - Install/update Python dependencies
- `make dev` - Start the FastAPI development server
- `make build` - Prepare for production deployment
- `make test` - Run backend tests
- `make clean` - Remove virtual environment and clean build artifacts
- `make format` - Format code with Black and isort
- `make lint` - Lint code with flake8

## Frontend Makefile

Located in the `frontend/` directory, this Makefile manages the React/TypeScript frontend.

### Available Commands:

- `make install` - Install Node.js dependencies
- `make dev` - Start the Vite development server
- `make build` - Build for production
- `make preview` - Preview the production build
- `make test` - Run frontend tests
- `make clean` - Remove node_modules and build artifacts
- `make format` - Format code with Prettier
- `make lint` - Lint code with ESLint
- `make type-check` - Run TypeScript type checking

## Getting Started

1. Install dependencies:
   ```bash
   make install
   ```

2. Start development servers:
   ```bash
   make dev
   ```

3. Access the application:
   - Frontend: http://localhost:5173
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

## Development Workflow

- Use `make format` and `make lint` to maintain code quality
- Run `make test` before committing changes
- For production builds, use `make build`

## Cleanup

To clean up all build artifacts and start fresh:

```bash
make clean
```
