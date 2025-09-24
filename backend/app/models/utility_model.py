from pydantic import BaseModel


# Request models
class SendEmailRequest(BaseModel):
    """Request model for sending email endpoints""" 
    name: str
    email: str
    message: str

# Response models

class VideoResponse(BaseModel):
    """Response model for getting latest videos endpoints"""
    video_id: str
    title: str


class SendEmailResponse(BaseModel):
    """Response model for sending email endpoints"""
    status: str
    message: str
