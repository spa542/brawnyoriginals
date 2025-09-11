import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from pathlib import Path

app = FastAPI(
    title="Brawny Originals API",
    description="Backend API and Frontend for Brawny Originals",
    version="0.1.0",
    docs_url="/api/docs",
    openapi_url="/api/openapi.json"
)

# Configure CORS in development
if os.getenv("ENV") == "development":
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:5173"],  # Vite default port
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

# Mount static files in production
if os.getenv("ENV") == "production":
    frontend_path = Path(__file__).parent.parent / "frontend" / "dist"
    if frontend_path.exists():
        # Mount static files to /static
        app.mount("/static", StaticFiles(directory=str(frontend_path), html=True), name="static")
        
        # Serve index.html for all non-API routes
        @app.get("/{full_path:path}")
        async def serve_spa(full_path: str):
            # Don't interfere with API routes
            if full_path.startswith("api/"):
                return {"message": "Not Found"}, 404
                
            # Check if the requested file exists in static assets
            static_file = frontend_path / full_path
            if static_file.exists() and static_file.is_file():
                return FileResponse(static_file)
                
            # Default to index.html for SPA routing
            return FileResponse(frontend_path / "index.html")

class HealthCheckResponse(BaseModel):
    status: str
    message: str

@app.get("/api/health", response_model=HealthCheckResponse, tags=["Health"])
async def health_check():
    """Health check endpoint"""
    return {
        "status": "ok",
        "message": "Service is up and running"
    }

@app.get("/api/hello/{name}")
async def say_hello(name: str):
    """Example endpoint with a path parameter"""
    return {"message": f"Hello, {name}!"}

if __name__ == "__main__":
    import uvicorn
    env = os.getenv("ENV", "development")
    reload = env == "development"
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=int(os.getenv("PORT", "8000")),
        reload=reload,
        workers=4 if env == "production" else 1
    )
