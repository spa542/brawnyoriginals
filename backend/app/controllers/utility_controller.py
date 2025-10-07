import os
import requests
from typing import Dict, Any

from fastapi import HTTPException, status

from app.utilities.helpers import is_dev, get_cfg
from app.models.utility_model import SendEmailResponse, VideoResponse
from app.utilities.recaptcha import verify_recaptcha_token
from app.utilities.logger import get_logger
from app.utilities.doppler_utils import get_doppler_secret
from app.utilities.youtube_utils import get_latest_short, get_latest_video


async def scrape_latest_youtube_video() -> VideoResponse:
    """
    Fetch the latest video from the YouTube channel.
    
    Returns:
        VideoResponse: Object containing video ID
        
    Raises:
        HTTPException: If there's an error fetching the video
    """
    logger = get_logger(__name__)
    logger.info("Fetching latest YouTube video")
    
    try:
        video = await get_latest_video()
        
        if not video:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No videos found"
            )
            
        result = VideoResponse(video_id=video["id"])
        logger.debug("Successfully fetched YouTube video", extra={"video_id": result.video_id})
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Failed to fetch YouTube video", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch latest YouTube video"
        )


async def scrape_latest_youtube_short() -> VideoResponse:
    """
    Fetch the latest YouTube short from the channel.
    
    Returns:
        VideoResponse: Object containing short video ID
        
    Raises:
        HTTPException: If there's an error fetching the short
    """
    logger = get_logger(__name__)
    logger.info("Fetching latest YouTube short")
    
    try:
        video = await get_latest_short()
        
        if not video:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No shorts found"
            )
            
        result = VideoResponse(video_id=video["id"])
        logger.debug("Successfully fetched YouTube short", extra={"video_id": result.video_id})
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Failed to fetch YouTube short", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch latest YouTube short"
        )


def scrape_latest_tiktok_video() -> Dict[str, Any]:
    """
    Scrape the latest video from the specified URL.
    
    Returns:
        Dict containing video ID and title
    """
    logger = get_logger(__name__)
    logger.info("Fetching latest TikTok video")
    
    try:
        # NOTE: Fow now, TikTok public API is not available and web scrapers are unreliable. Hardcoding for now 
        result = VideoResponse(
            video_id="7556011260790328606",
        )
        logger.debug("Successfully fetched TikTok video", extra={"video_id": result.video_id})
        return result
    except Exception as e:
        logger.error("Failed to fetch TikTok video", exc_info=True)
        raise


async def send_email(name: str, email: str, message: str, g_recaptcha_response: str) -> Dict[str, Any]:
    """
    Send email to the specified email address.
    
    Args:
        name: Name of the sender
        email: Email address of the sender
        message: Email message content
        g_recaptcha_response: reCAPTCHA response token
    Returns:
        Dict containing status and message
        
    Raises:
        ValueError: If there's an error sending the email
    """
    logger = get_logger(__name__)
    logger.info("Processing email send request", extra={"email": email})
    
    # Verify reCAPTCHA token
    try:
        is_valid = await verify_recaptcha_token(g_recaptcha_response)
        if not is_valid:
            logger.warning("reCAPTCHA verification failed", extra={"email": email})
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="reCAPTCHA verification failed"
            )
        logger.debug("reCAPTCHA verification successful", extra={"email": email})
    except Exception as e:
        logger.error("Error during reCAPTCHA verification", exc_info=True, extra={"email": email})
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error during reCAPTCHA verification"
        )

    # Get config file
    cfg = get_cfg()
    # Setup email variables
    url = cfg.get("MAILGUN", "url")
    email_from = ("Mailgun Sandbox" if is_dev() else "Mailgun Production") + f" <{cfg.get('MAILGUN', 'from_uri')}>"
    email_to = cfg.get("MAILGUN", "contact_email")

    try:
        mailgun_api_key = await get_doppler_secret("MAILGUN_API_KEY")
        auth = ("api", mailgun_api_key)
    except Exception as e:
        logger.error(f"Failed to get Mailgun API key from Doppler: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Email service configuration error"
        )
        
    try:
        # TODO Adjust email message based on type of email being sent
        data = {
            "from": email_from,
            "to": email_to,
            "subject": f"Brawny Originals - Contact Form - Message from {name} <{email}>",
            "text": message
        }

        logger.debug("Sending email", extra={"to": email_to, "subject": data["subject"]})
        
        # Send the email
        response = requests.post(url, auth=auth, data=data, timeout=10)
        response.raise_for_status()
        
        logger.info("Email sent successfully", extra={"to": email_to, "email": email})
        
        return SendEmailResponse(
            status="success",
            message="Email sent successfully"
        )
        
    except requests.exceptions.RequestException as e:
        logger.error("Failed to send email", exc_info=True, extra={"email": email, "to": email_to})
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to send email"
        )
