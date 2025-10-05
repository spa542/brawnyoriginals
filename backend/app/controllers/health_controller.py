from app.models.health_model import HealthCheckResponse
from app.utilities.logger import get_logger


def health_check() -> HealthCheckResponse:
    """
    Health check endpoint handler
    Returns:
        HealthCheckResponse: Health status response
    """
    logger = get_logger(__name__)
    logger.info("Health check requested")
    
    try:
        response = HealthCheckResponse(
            status="ok",
            message="Service is up and running"
        )
        logger.debug("Health check completed successfully")
        return response
    except Exception as e:
        logger.error("Health check failed", exc_info=True)
        raise
