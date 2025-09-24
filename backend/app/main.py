"""
Main FastAPI application setup and configuration.
"""
import os
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError, HTTPException
import uvicorn

from app.routers import core_router, health_router
from app.models.core_model import ErrorResponse


def create_app() -> FastAPI:
    """
    Create and configure the FastAPI application.
    
    Returns:
        FastAPI: Configured FastAPI application instance
    """
    # Initialize FastAPI app
    app = FastAPI(
        title="Brawny Originals API",
        description="Backend API and Frontend for Brawny Originals",
        version="0.1.0",
        docs_url="/api/docs",
        openapi_url="/api/openapi.json"
    )
    
    
    # Add exception handlers
    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(
        request: Request, exc: RequestValidationError
    ) -> JSONResponse:
        """Handle validation errors"""
        return JSONResponse(
            status_code=422,
            content=ErrorResponse(
                detail="Validation error",
                error=str(exc),
                status_code=422
            ).dict()
        )

    @app.exception_handler(HTTPException)
    async def http_exception_handler(
        request: Request, exc: HTTPException
    ) -> JSONResponse:
        """Handle HTTP exceptions"""
        return JSONResponse(
            status_code=exc.status_code,
            content=ErrorResponse(
                detail=exc.detail,
                error=str(exc),
                status_code=exc.status_code
            ).model_dump()
        )

    @app.exception_handler(Exception)
    async def general_exception_handler(
        request: Request, exc: Exception
    ) -> JSONResponse:
        """Handle all other exceptions"""
        return JSONResponse(
            status_code=500,
            content=ErrorResponse(
                detail="Internal server error",
                error=str(exc),
                status_code=500
            ).model_dump()
        )
    
    # Include routers
    app.include_router(core_router.router)
    app.include_router(health_router.router, prefix="/api")

    env = os.getenv("ENV")

    # Configure CORS in development
    if env == "development":
        app.add_middleware(
            CORSMiddleware,
            allow_origins=["http://localhost:5173"],  # Vite default port
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
    elif env == "production":  # Mount static files in production
        # Path to the frontend build directory
        frontend_path = Path(__file__).parent.parent.parent / "frontend" / "dist"
        
        # Mount static files
        app.mount(
            "/static",
            StaticFiles(directory=str(frontend_path), html=True),
            name="static"
        )
    else:
        raise ValueError(f"Invalid environment set: {env}")
    
    return app


# Create the FastAPI application
app = create_app()


# This allows the app to be run directly with: python -m app.main
if __name__ == "__main__":
    env = os.getenv("ENV", "development")
    reload = env == "development"
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=reload,
        workers=4 if env == "production" else 1
    )
