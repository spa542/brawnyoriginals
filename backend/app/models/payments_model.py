from pydantic import BaseModel, HttpUrl, field_validator
from typing import List, Dict, Any
from datetime import datetime, timezone
from app.utilities.helpers import get_cfg


# Helpers

def _get_valid_price_ids() -> List[str]:
    """Get valid price IDs from config.
    
    Returns:
        List of valid price IDs from the configuration
    """
    cfg = get_cfg()
    price_ids_str = cfg.get('STRIPE', 'valid_price_ids', fallback='')
    return [pid.strip() for pid in price_ids_str.split(',') if pid.strip()]


def _validate_price_ids(price_ids: List[str]) -> List[str]:
    """Validate a price ID against the configured valid price IDs.
    
    Args:
        price_id: The price ID to validate
        
    Returns:
        The validated price ID if valid
        
    Raises:
        ValueError: If the price ID is not in the valid list or if no valid IDs are configured
    """
    valid_ids = _get_valid_price_ids()
    if not valid_ids:
        raise ValueError('No valid price IDs configured')
    for price_id in price_ids:
        if price_id not in valid_ids:
            raise ValueError(f'Invalid price ID: {price_id}. Must be one of {valid_ids}')
    return price_ids 


# Request Models

class CreateCheckoutSessionRequest(BaseModel):
    """Request model for creating a checkout session."""
    token: str  # HMAC token from /payments/generate-token
    price_ids: List[str]  # List of Stripe price IDs for the products
    quantity: int = 1  # Number of items to purchase (min: 1)
    success_url: HttpUrl  # URL to redirect after successful payment
    cancel_url: HttpUrl  # URL to redirect if payment is cancelled

    @field_validator('price_ids')
    def validate_price_ids(cls, v):
        return _validate_price_ids(v)


class CheckoutTokenRequest(BaseModel):
    """Request model for generating a checkout token."""
    price_ids: List[str]  # List of Stripe price IDs for the products
    captcha_token: str  # CAPTCHA token for verification

    @field_validator('price_ids')
    def validate_price_ids(cls, v):
        return _validate_price_ids(v) 


# Response Models

class CheckoutSessionResponse(BaseModel):
    """Response model for a created checkout session."""
    session_id: str  # Stripe session ID
    url: str  # Checkout URL
    expires_at: int  # Unix timestamp
    payment_status: str  # Current payment status


class WebhookResponse(BaseModel):
    """Response model for webhook handling."""
    received: bool  # Whether the webhook was received
    event_type: str  # Type of Stripe event
    event_id: str  # Unique event ID from Stripe


class CheckoutTokenResponse(BaseModel):
    """Response model containing the generated checkout token."""
    token: str  # HMAC token for checkout
    expires_at: int  # Unix timestamp when token expires


# Event Models

class WebhookEvent(BaseModel):
    """Base model for Stripe webhook events."""
    id: str
    type: str
    data: Dict[str, Any]
    created: int
    api_version: str


# Extra Data Models

class CheckoutTokenData(BaseModel):
    """Data model for the checkout token payload."""
    price_ids: List[str]  # List of Stripe price IDs
    created_at: int  # Timestamp when token was created
    expires_at: int  # Timestamp when token expires

    @field_validator('price_ids')
    def validate_price_ids(cls, v):
        return _validate_price_ids(v)

    @classmethod
    def from_request(
        cls,
        request: 'CheckoutTokenRequest',
        token_lifetime_seconds: int = 300  # 5 minutes
    ) -> 'CheckoutTokenData':
        """Create token data from a token request."""
        now = int(datetime.now(timezone.utc).timestamp())
        return cls(
            price_ids=request.price_ids,
            created_at=now,
            expires_at=now + token_lifetime_seconds
        )

    def is_expired(self) -> bool:
        """Check if the token has expired."""
        return datetime.now(timezone.utc).timestamp() > self.expires_at
