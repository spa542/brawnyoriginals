import logging
import httpx

from fastapi import HTTPException

from app.utilities.logger import get_logger
from app.utilities.doppler_utils import get_doppler_secret
from app.utilities.helpers import is_dev


RECAPTCHA_VERIFY_URL = "https://www.google.com/recaptcha/api/siteverify"


async def verify_recaptcha_token(token: str) -> bool:
    """
    Verify a reCAPTCHA token with Google's reCAPTCHA API.
    
    Args:
        token: The reCAPTCHA token from the client
        
    Returns:
        bool: True if the token is valid, False otherwise
        
    Raises:
        HTTPException: If there's an error during verification
    """
    
    # Initialize logger inside the function
    try:
        logger = get_logger(__name__)
    except Exception as e:
        # Fallback to basic logger if there's an issue with the custom logger
        logging.basicConfig(level=logging.INFO)
        logger = logging.getLogger(__name__)
        logger.warning(f"Failed to initialize custom logger: {e}")
    
    try:
        RECAPTCHA_SECRET_KEY = await get_doppler_secret("CAPTCHA_SECRET_KEY")
    except Exception as e:
        logger.error(f"Failed to get reCAPTCHA secret key from Doppler: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Server configuration error: reCAPTCHA secret key not configured"
        )
    
    if not token:
        logger.warning("No reCAPTCHA token provided")
        return False
    
    try:
        async with httpx.AsyncClient() as client:
            logger.debug(f"Sending reCAPTCHA verification request for token: {token[:10]}...")
            response = await client.post(
                RECAPTCHA_VERIFY_URL,
                data={
                    "secret": RECAPTCHA_SECRET_KEY,
                    "response": token
                },
                timeout=15
            )
            
            logger.debug(f"reCAPTCHA API response status: {response.status_code}")
            
            try:
                result = response.json()
                logger.debug(f"reCAPTCHA API response: {result}")
                
                if not isinstance(result, dict):
                    logger.error(f"Unexpected response format from reCAPTCHA API: {result}")
                    return False
                
                if 'success' not in result:
                    logger.error(f"Missing 'success' field in reCAPTCHA response: {result}")
                    return False
                
                if not result['success']:
                    error_codes = result.get('error-codes', [])
                    logger.warning(f"reCAPTCHA verification failed. Error codes: {error_codes}")
                    return False
                
                score = result.get('score', 0)
                logger.info(f"reCAPTCHA verification successful. Score: {score}")
                
                # Bypass reCAPTCHA verification in development mode if is_dev() - Letting the above code run for testing purposes
                if is_dev():
                    logger.info("Development mode: Bypassing reCAPTCHA verification")
                    return True

                return score >= 0.5  # Adjust threshold as needed
                
            except ValueError as e:
                logger.error(f"Error parsing reCAPTCHA response: {str(e)}. Response content: {response.text}")
                return False
                
    except httpx.TimeoutException:
        logger.error("reCAPTCHA verification request timed out")
        return False
    except Exception as e:
        logger.error(f"Unexpected error during reCAPTCHA verification - Error: {str(e)}, Type: {type(e).__name__}")
        return False
