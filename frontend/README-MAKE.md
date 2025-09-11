# Frontend Makefile Documentation

This document describes the available make targets for the React/TypeScript frontend.

## Development

### `make install`
Installs all Node.js dependencies using npm.
- Creates/updates `node_modules`
- Installs all dependencies from `package.json`

### `make dev`
Starts the Vite development server with hot module replacement.
- **Access App**: http://localhost:5173
- **Features**: Hot reloading, source maps, and development tools

## Build & Preview

### `make build`
Builds the application for production.
- Optimized and minified assets
- Outputs to `dist/` directory

### `make preview`
Serves the production build locally for testing.
- Requires `make build` to be run first
- Serves from the `dist/` directory

## Code Quality

### `make format`
Formats code using Prettier.
- Applies consistent code style
- Modifies files in place

### `make lint`
Runs ESLint to check for code quality issues.
- Reports potential problems
- Follows project's ESLint configuration

### `make type-check`
Runs TypeScript type checking.
- Verifies type safety
- No code is emitted

## Testing

### `make test`
Runs the test suite.
- Uses the project's test runner (e.g., Vitest, Jest)
- Watches for changes in test files

## Cleanup

### `make clean`
Removes:
- `node_modules/` directory
- Build output (`dist/`)
- Cache directories (`.next/`, `.turbo/`)
- Lock files (`package-lock.json`, `yarn.lock`, `pnpm-lock.yaml`)

## Environment Variables

The following environment variables can be configured:
- `PORT`: Port for the development server (default: 5173)
- `NODE_ENV`: Environment mode (development/production)

## Usage Example

```bash
# First time setup
make install

# Start development server
make dev

# Run linter and type checker
make lint
make type-check

# Build for production
make build
make preview

# Clean up
make clean
```

## Development Workflow

1. Make your changes to the source files
2. Run `make format` to format your code
3. Run `make lint` and `make type-check` to catch issues
4. Run `make test` to ensure tests pass
5. Start the dev server with `make dev` to test your changes
6. Create a production build with `make build` when ready to deploy
