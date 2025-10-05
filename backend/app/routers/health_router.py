from fastapi import APIRouter

import app.controllers.health_controller as hc
from app.models.health_model import HealthCheckResponse
from app.utilities.logger import get_logger

router = APIRouter()

@router.get(
    "/health",
    response_model=HealthCheckResponse,
    status_code=200,
    tags=["Health"]
)
async def health_check():
    """
    Health check endpoint
    Returns:
        HealthCheckResponse: Health status of the service
    """
    logger = get_logger(__name__)
    logger.info("Health check endpoint called")
    
    try:
        result = hc.health_check()
        logger.debug("Health check completed", extra={"status": result.status})
        return result
    except Exception as e:
        logger.error("Health check endpoint failed", exc_info=True)
        raise
