from pydantic import BaseModel, EmailStr


# Request models

class SendEmailRequest(BaseModel):
    """Request model for sending email endpoints""" 
    name: str
    email: EmailStr
    message: str
    g_recaptcha_response: str 


# Response models

class VideoResponse(BaseModel):
    """Response model for getting latest videos endpoints"""
    video_id: str


class SendEmailResponse(BaseModel):
    """Response model for sending email endpoints"""
    status: str
    message: str
