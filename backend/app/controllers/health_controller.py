from app.models.health_model import HealthCheckResponse


def health_check() -> HealthCheckResponse:
    """
    Health check endpoint handler
    Returns:
        HealthCheckResponse: Health status response
    """
    return HealthCheckResponse(
        status="ok",
        message="Service is up and running"
    )
