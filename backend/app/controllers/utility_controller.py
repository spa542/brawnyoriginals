from typing import Dict, Any

from fastapi import HTTPException, status

from app.models.utility_model import SendContactEmailResponse, VideoResponse
from app.utilities.logger import get_logger
from app.utilities.youtube_utils import get_latest_short, get_latest_video
from app.utilities.email import send_email_util


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
        logger.debug(f"Successfully fetched YouTube video with ID: {result.video_id}")
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to fetch YouTube video: {str(e)}")
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
        logger.debug(f"Successfully fetched YouTube short with ID: {result.video_id}")
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to fetch YouTube short: {str(e)}")
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
        logger.debug(f"Successfully fetched TikTok video with ID: {result.video_id}")
        return result
    except Exception as e:
        logger.error(f"Failed to fetch TikTok video: {str(e)}")
        raise


async def send_contact_email(name: str, email: str, message: str) -> Dict[str, Any]:
    """
    Send email to the specified email address.
    
    Args:
        name: Name of the sender
        email: Email address of the sender
        message: Email message content
        
    Returns:
        Dict containing status and message
        
    Raises:
        HTTPException: If there's an error sending the email
    """
    logger = get_logger(__name__)
    logger.info(f"Processing email send request from: {email}")
    
    try:
        response = await send_email_util(name, email, message, mode="contact")
        return SendContactEmailResponse(**response)
    except HTTPException:
        # Re-raise HTTP exceptions from the utility
        raise
    except Exception as e:
        logger.error(f"Unexpected error in send_contact_email: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while sending the email"
        )
