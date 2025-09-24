from fastapi import APIRouter

import app.controllers.utility_controller as uc
from app.models.utility_model import UtilityVideoResponse


router = APIRouter()


@router.get(
    "/latest/youtube",
    response_model=UtilityVideoResponse,
    status_code=200,
    tags=["Utility"]
)
async def retrieve_latest_youtube_video():
    """Health check endpoint"""
    return None


@router.get(
    "/latest/short",
    response_model=UtilityVideoResponse,
    status_code=200,
    tags=["Utility"]
)
async def retrieve_latest_youtube_short():
    """Health check endpoint"""
    return None


@router.get(
    "/latest/tiktok",
    response_model=UtilityVideoResponse,
    status_code=200,
    tags=["Utility"]
)
async def retrieve_latest_tiktok():
    """Health check endpoint"""
    return None
