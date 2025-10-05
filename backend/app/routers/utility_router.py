import traceback
from fastapi import APIRouter, HTTPException, status

import app.controllers.utility_controller as uc
from app.models.utility_model import VideoResponse, SendEmailResponse, SendEmailRequest
from app.utilities.logger import get_logger


router = APIRouter()


@router.get(
    "/latest/youtube",
    response_model=VideoResponse,
    status_code=200,
    tags=["Utility"]
)
async def retrieve_latest_youtube_video():
    """Retrieve the latest YouTube video"""
    logger = get_logger(__name__)
    logger.info("Fetching latest YouTube video")
    try:
        result = await uc.scrape_latest_youtube_video()
        logger.debug("Successfully fetched YouTube video", extra={"video_id": result.video_id})
        return result
    except Exception as e:
        logger.error("Failed to fetch YouTube video", exc_info=True)
        raise


@router.get(
    "/latest/short",
    response_model=VideoResponse,
    status_code=200,
    tags=["Utility"]
)
async def retrieve_latest_youtube_short():
    """Retrieve the latest YouTube short"""
    logger = get_logger(__name__)
    logger.info("Fetching latest YouTube short")
    try:
        result = await uc.scrape_latest_youtube_short()
        logger.debug("Successfully fetched YouTube short", extra={"video_id": result.video_id})
        return result
    except Exception as e:
        logger.error("Failed to fetch YouTube short", exc_info=True)
        raise


@router.get(
    "/latest/tiktok",
    response_model=VideoResponse,
    status_code=200,
    tags=["Utility"]
)
async def retrieve_latest_tiktok():
    """Retrieve the latest TikTok video"""
    logger = get_logger(__name__)
    logger.info("Fetching latest TikTok video")
    try:
        result = uc.scrape_latest_tiktok_video()
        logger.debug("Successfully fetched TikTok video", extra={"video_id": result.video_id})
        return result
    except Exception as e:
        logger.error("Failed to fetch TikTok video", exc_info=True)
        raise


@router.post(
    "/contact/email",
    response_model=SendEmailResponse,
    status_code=200,
    tags=["Utility"]
)
async def send_email(request: SendEmailRequest):
    """Send email to the specified email address"""
    logger = get_logger(__name__)
    logger.info("Processing email send request", extra={"email": request.email})
    
    try:
        result = await uc.send_email(**request.model_dump())
        logger.info("Email sent successfully", extra={"email": request.email})
        return result
    except HTTPException as he:
        logger.warning(
            "Email send failed with HTTP exception", 
            extra={"status_code": he.status_code, "detail": he.detail},
            exc_info=True
        )
        raise
    except Exception as e:
        error_detail = f'{str(e)}\n\n{traceback.format_exc()}'
        logger.error(
            "Unexpected error sending email", 
            extra={"error": str(e), "error_type": type(e).__name__},
            exc_info=True
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail=error_detail
        ) 
