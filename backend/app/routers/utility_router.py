from fastapi import APIRouter

import app.controllers.utility_controller as uc
from app.models.utility_model import VideoResponse, SendEmailResponse, SendEmailRequest


router = APIRouter()


@router.get(
    "/latest/youtube",
    response_model=VideoResponse,
    status_code=200,
    tags=["Utility"]
)
async def retrieve_latest_youtube_video():
    return uc.scrape_latest_youtube_video()


@router.get(
    "/latest/short",
    response_model=VideoResponse,
    status_code=200,
    tags=["Utility"]
)
async def retrieve_latest_youtube_short():
    return uc.scrape_latest_youtube_short()


@router.get(
    "/latest/tiktok",
    response_model=VideoResponse,
    status_code=200,
    tags=["Utility"]
)
async def retrieve_latest_tiktok():
    return uc.scrape_latest_tiktok_video()


@router.post(
    "/contact/email",
    response_model=SendEmailResponse,
    status_code=200,
    tags=["Utility"]
)
async def send_email(request: SendEmailRequest):
    """Send email to the specified email address"""
    return uc.send_email(**request.model_dump())
