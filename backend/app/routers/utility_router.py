import traceback
from fastapi import APIRouter, HTTPException, status

import app.controllers.utility_controller as uc
from app.models.utility_model import VideoResponse, SendContactEmailResponse, SendContactEmailRequest
from app.utilities.logger import get_logger
from app.utilities.recaptcha import verify_recaptcha_token


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
    response_model=SendContactEmailResponse,
    status_code=200,
    tags=["Utility"]
)
async def send_contact_email(request: SendContactEmailRequest):
    """
    Send contact email.
    
    This endpoint verifies the reCAPTCHA token before processing the email.
    """
    logger = get_logger(__name__)
    logger.info("Processing email send request", extra={"email": request.email})
    
    # Verify reCAPTCHA token
    try:
        is_valid = await verify_recaptcha_token(request.g_recaptcha_response)
        if not is_valid:
            logger.warning("reCAPTCHA verification failed", extra={"email": request.email})
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="reCAPTCHA verification failed"
            )
        logger.debug("reCAPTCHA verification successful", extra={"email": request.email})
    except Exception as e:
        logger.error("Error during reCAPTCHA verification", exc_info=True, extra={"email": request.email})
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error during reCAPTCHA verification"
        )
    
    try:
        # Extract only the needed fields for the controller
        email_data = {
            'name': request.name,
            'email': request.email,
            'message': request.message
        }
        result = await uc.send_contact_email(**email_data)
        logger.info("Contact email sent successfully", extra={"email": request.email})
        return result
    except HTTPException as he:
        logger.warning(
            "Contact email send failed with HTTP exception", 
            extra={"status_code": he.status_code, "detail": he.detail},
            exc_info=True
        )
        raise
    except Exception as e:
        error_detail = f'{str(e)}\n\n{traceback.format_exc()}'
        logger.error(
            "Unexpected error sending contact email", 
            extra={"error": str(e), "error_type": type(e).__name__},
            exc_info=True
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail=error_detail
        ) 
