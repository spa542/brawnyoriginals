import traceback
from fastapi import APIRouter, HTTPException, status, Request

import app.controllers.utility_controller as uc
from app.models.utility_model import VideoResponse, SendContactEmailResponse, SendContactEmailRequest
from app.utilities.logger import get_logger
from app.utilities.recaptcha import verify_recaptcha_token
from app.utilities.rate_limiter import limiter


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
        logger.debug(f"Successfully fetched YouTube video - Video ID: {result.video_id}")
        return result
    except Exception as e:
        logger.error("Failed to fetch YouTube video")
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
        logger.debug(f"Successfully fetched YouTube short - Video ID: {result.video_id}")
        return result
    except Exception as e:
        logger.error("Failed to fetch YouTube short")
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
        logger.debug(f"Successfully fetched TikTok video - Video ID: {result.video_id}")
        return result
    except Exception as e:
        logger.error("Failed to fetch TikTok video")
        raise


@router.post(
    "/contact/email",
    response_model=SendContactEmailResponse,
    status_code=200,
    tags=["Utility"]
)
@limiter.limit("3/minute")
async def send_contact_email(
    request: Request,
    contact_request: SendContactEmailRequest
):
    """
    Send contact email.
    
    This endpoint verifies the reCAPTCHA token before processing the email.
    """
    logger = get_logger(__name__)
    logger.info(f"Processing email send request from: {contact_request.email}")
    
    # Verify reCAPTCHA token
    try:
        is_valid = await verify_recaptcha_token(contact_request.g_recaptcha_response)
        if not is_valid:
            logger.warning(f"reCAPTCHA verification failed - Email: {contact_request.email}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="reCAPTCHA verification failed"
            )
        logger.debug(f"reCAPTCHA verification successful - Email: {contact_request.email}")
    except Exception as e:
        logger.error(f"Error during reCAPTCHA verification - Email: {contact_request.email}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error during reCAPTCHA verification"
        )
    
    try:
        # Extract only the needed fields for the controller
        email_data = {
            'name': contact_request.name,
            'email': contact_request.email,
            'message': contact_request.message
        }
        result = await uc.send_contact_email(**email_data)
        logger.info(f"Contact email sent successfully - Email: {contact_request.email}")
        return result
    except HTTPException as he:
        logger.warning(
            f"Contact email send failed with HTTP exception - Status Code: {he.status_code}, Detail: {he.detail}"
        )
        raise
    except Exception as e:
        error_detail = f'{str(e)}\n\n{traceback.format_exc()}'
        logger.error(
            f"Unexpected error sending contact email - Error: {str(e)}, Type: {type(e).__name__}"
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail=error_detail
        ) 
