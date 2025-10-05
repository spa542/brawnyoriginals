from pathlib import Path

from fastapi import APIRouter
from fastapi.responses import FileResponse

router = APIRouter()


# Get the root directory of the project
BASE_DIR = Path(__file__).parent.parent.parent.parent


@router.get("/")
async def serve_frontend():
    """Serve the frontend's index.html file"""
    # Path to the frontend's dist directory
    frontend_path = BASE_DIR / "frontend" / "dist"
    index_path = frontend_path / "index.html"
    
    # Check if the file exists
    if not index_path.exists():
        return {"error": "Frontend not built. Please run 'npm run build' in the frontend directory."}
    
    return FileResponse(index_path)
