import hmac
import hashlib
import base64
import json
from typing import Dict, Any, Optional, Union

from app.utilities.doppler_utils import get_doppler_secret
from app.utilities.logger import get_logger


async def generate_hmac_token(
    data: Dict[str, Any]
) -> str:
    """
    Generate an HMAC token for the given data.
    
    Args:
        data: Data to include in the token
        
    Returns:
        str: Base64 encoded HMAC token
        
    Raises:
        RuntimeError: If HMAC secret cannot be retrieved from Doppler
    """
    logger = get_logger(__name__)
    
    # Get HMAC secret from Doppler
    try:
        secret_str = await get_doppler_secret("HMAC_SECRET_KEY")
        secret = secret_str.encode('utf-8')
    except Exception as e:
        logger.error("Failed to retrieve HMAC_SECRET_KEY from Doppler", exc_info=True)
        raise RuntimeError("Failed to retrieve HMAC secret from Doppler") from e
    
    # Convert data to JSON and encode to bytes
    json_data = json.dumps(data, sort_keys=True).encode('utf-8')
    
    try:
        # Create HMAC signature
        signature = hmac.new(
            secret,
            json_data,
            hashlib.sha256
        ).digest()
        
        # Combine data and signature
        token_data = {
            'data': data,
            'signature': base64.b64encode(signature).decode('utf-8')
        }
        
        # Return base64 encoded token
        return base64.b64encode(json.dumps(token_data).encode('utf-8')).decode('utf-8')
        
    except Exception as e:
        logger.error(f"Error generating HMAC token: {str(e)}", exc_info=True)
        raise


async def verify_hmac_token(
    token: str,
    current_time: Optional[float] = None
) -> Dict[str, Any]:
    """
    Verify an HMAC token and return the decoded data if valid.
    
    Args:
        token: Base64 encoded HMAC token
        current_time: Optional timestamp to use for expiration check (for testing)
        
    Returns:
        Dict containing the decoded token data
        
    Raises:
        ValueError: If the token is invalid, expired, or verification fails
        RuntimeError: If HMAC secret cannot be retrieved from Doppler
    """
    logger = get_logger(__name__)
    
    # Get HMAC secret from Doppler
    try:
        secret_str = await get_doppler_secret("HMAC_SECRET_KEY")
        secret = secret_str.encode('utf-8')
    except Exception as e:
        logger.error("Failed to retrieve HMAC_SECRET_KEY from Doppler", exc_info=True)
        raise RuntimeError("Failed to retrieve HMAC secret from Doppler") from e
    
    if current_time is None:
        import time
        current_time = time.time()
    
    try:
        # Decode the token
        token_data = json.loads(base64.b64decode(token).decode('utf-8'))
        
        # Verify required fields
        if not isinstance(token_data, dict) or 'data' not in token_data or 'signature' not in token_data:
            raise ValueError("Invalid token format")
        
        # Recreate the signature
        json_data = json.dumps(token_data['data'], sort_keys=True).encode('utf-8')
        expected_signature = hmac.new(
            secret,
            json_data,
            hashlib.sha256
        ).digest()
        
        # Compare signatures
        provided_signature = base64.b64decode(token_data['signature'].encode('utf-8'))
        if not hmac.compare_digest(expected_signature, provided_signature):
            raise ValueError("Invalid token signature")
        
        # Check if token is expired
        if 'expires_at' in token_data['data'] and token_data['data']['expires_at'] < current_time:
            raise ValueError("Token has expired")
        
        return token_data['data']
        
    except (json.JSONDecodeError, UnicodeDecodeError, base64.binascii.Error) as e:
        raise ValueError(f"Invalid token encoding: {str(e)}")
    except Exception as e:
        logger.warning("Token verification failed: %s", str(e))
        raise
