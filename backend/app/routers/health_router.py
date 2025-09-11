from fastapi import APIRouter

from app.controllers.core_controller import CoreController
from app.models.core_model import HealthCheckResponse

router = APIRouter()
controller = CoreController()

@router.get(
    "/health",
    response_model=HealthCheckResponse,
    status_code=200,
    tags=["Health"]
)
async def health_check():
    """Health check endpoint"""
    return controller.health_check()
