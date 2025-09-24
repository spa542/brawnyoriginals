from pydantic import BaseModel


class UtilityVideoResponse(BaseModel):
    """Response model for health check endpoint"""
    video_id: str
    title: str
