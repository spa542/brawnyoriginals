from fastapi import APIRouter

import app.controllers.health_controller as hc
from app.models.health_model import HealthCheckResponse


router = APIRouter()


@router.get(
    "/health",
    response_model=HealthCheckResponse,
    status_code=200,
    tags=["Health"]
)
async def health_check():
    """Health check endpoint"""
    return hc.health_check()
