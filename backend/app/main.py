"""
Main FastAPI application setup and configuration.
"""
import os
from pathlib import Path
import logging

from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError, HTTPException
from app.utilities.rate_limiter import limiter, export_rate_limit_exceeded_handler, export_RateLimitExceeded as RateLimitExceeded
import uvicorn

from app.routers import core_router, health_router, utility_router, payments_router
from app.models.core_model import ErrorResponse
from app.utilities.helpers import is_dev, is_prod, is_valid_environment
from app.utilities.logger import init_logger


def create_app() -> FastAPI:
    """
    Create and configure the FastAPI application.
    
    Returns:
        FastAPI: Configured FastAPI application instance
    """
    # Initialize logger
    log_level = logging.DEBUG if is_dev() else logging.INFO
    init_logger(log_level=log_level)
    
    # Initialize FastAPI app
    app = FastAPI(
        title="Brawny Originals API",
        description="API for Brawny Originals application",
        version="1.0.0",
        docs_url="/api/docs" if is_dev() else None,
        redoc_url="/api/redoc" if is_dev() else None,
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
            ).model_dump()
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
        # Handle rate limit exceeded
        if isinstance(exc, RateLimitExceeded):
            return _rate_limit_exceeded_handler(request, exc)
            
        return JSONResponse(
            status_code=500,
            content=ErrorResponse(
                detail="Internal server error",
                error=str(exc),
                status_code=500
            ).model_dump()
        )
    
    # Configure rate limiter in the app
    app.state.limiter = limiter
    app.add_exception_handler(RateLimitExceeded, export_rate_limit_exceeded_handler)
    
    # Include routers
    app.include_router(core_router.router)
    app.include_router(health_router.router, prefix="/api")
    app.include_router(utility_router.router, prefix="/api")
    app.include_router(payments_router.router, prefix="/api") 

    # Check that environmetn is set and valid
    if not is_valid_environment():
        raise ValueError(f"Invalid environment set: {os.getenv('ENV')}")

    # Configure CORS in development
    if is_dev():
        app.add_middleware(
            CORSMiddleware,
            allow_origins=["http://localhost:5173"],  # Vite default port
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    if is_prod():  # Mount static files in production
        # Path to the frontend build directory
        frontend_path = Path(__file__).parent.parent.parent / "frontend" / "dist"
        
        # Mount static files
        app.mount(
            "/static",
            StaticFiles(directory=str(frontend_path), html=True),
            name="static"
        )
    
    return app


# Create the FastAPI application
app = create_app()


# This allows the app to be run directly with: python -m app.main
if __name__ == "__main__":
    reload = is_dev()
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=reload,
        workers=4 if is_prod() else 1
    )
