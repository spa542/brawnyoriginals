from pydantic import BaseModel
from typing import Optional


class ErrorResponse(BaseModel):
    """Standard error response model"""
    detail: str
    error: Optional[str] = None
    status_code: int
