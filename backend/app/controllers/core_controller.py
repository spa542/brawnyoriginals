from fastapi import HTTPException, status
from typing import Dict, Any

from app.models.core_model import HealthCheckResponse

class CoreController:
    """Core controller handling business logic for core endpoints"""
    
    @staticmethod
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
    
    @staticmethod
    def handle_404() -> Dict[str, Any]:
        """
        Handle 404 errors
        Returns:
            Dict with error details
        """
        return {
            "message": "Not Found"
        }
        
    @staticmethod
    def handle_500() -> Dict[str, Any]:
        """
        Handle 500 errors
        Returns:
            Dict with error details
        """
        return {
            "message": "Internal Server Error"
        }
