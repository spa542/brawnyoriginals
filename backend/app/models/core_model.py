from pydantic import BaseModel
from typing import Optional

class HealthCheckResponse(BaseModel):
    """Response model for health check endpoint"""
    status: str
    message: str

class ErrorResponse(BaseModel):
    """Standard error response model"""
    detail: str
    error: Optional[str] = None
    status_code: int
