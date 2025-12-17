from pydantic import BaseModel, HttpUrl, field_validator
from typing import List, Dict, Any, Literal
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


class PdfAttachment(BaseModel):
    """Model for PDF attachments in payment intents."""
    filename: str
    content: bytes
    content_type: Literal['application/pdf']


# NOTE: Update regularly as is required for payment intent fulfillment
PROGRAM_PI_MAPPING = {
    "price_1ScWdxK5tsm2JTU1Zogy9QKZ": "Program_Blue.pdf",  # Development
    "price_1Sf0Jj2cxMNEOVDK1vgR9A6A": "Program_Blue.pdf",  # Production
    "price_1ScWd9K5tsm2JTU1tjTXlwc8": "Program_Genesis.pdf",  # Development
    "price_1Sf0Js2cxMNEOVDKqVYTmhvZ": "Program_Genesis.pdf"  # Production
}


FULFILLMENT_EMAIL_BODY = """
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {
                font-family: Arial, sans-serif;
                line-height: 1.6;
                color: #333333;
                max-width: 600px;
                margin: 0 auto;
                padding: 20px;
            }
            .header {
                background-color: #1a1a1a;
                padding: 20px;
                text-align: center;
                margin-bottom: 20px;
            }
            .header h1 {
                color: #ffffff;
                margin: 0;
                font-size: 24px;
            }
            .content {
                background-color: #f9f9f9;
                padding: 25px;
                border-radius: 5px;
            }
            .footer {
                margin-top: 30px;
                font-size: 14px;
                color: #666666;
                text-align: center;
                padding-top: 20px;
                border-top: 1px solid #eeeeee;
            }
            .button {
                display: inline-block;
                background-color: #1a1a1a;
                color: #ffffff !important;
                padding: 12px 25px;
                text-decoration: none;
                border-radius: 4px;
                margin: 20px 0;
                font-weight: bold;
            }
            .program-list {
                margin: 20px 0;
                padding: 0;
                list-style: none;
            }
            .program-item {
                background: white;
                margin: 10px 0;
                padding: 15px;
                border-radius: 4px;
                border-left: 4px solid #1a1a1a;
            }
        </style>
    </head>
    <body>
        <div class="header">
            <h1>Your Brawny Originals Order Details</h1>
        </div>
        
        <div class="content">
            <h2>Thank you for your purchase!</h2>
            <p>Your order has been processed and we are excited to provide you with the following program(s) attached to help you on your fitness journey.</p>
            
            <p>To get started, simply download the attached program files. Each program includes detailed instructions and workout plans to help you achieve your fitness goals.</p>
            
            <p>If you have any questions about your programs or need assistance, please visit our <a href="https://www.brawnyoriginals.com/#/contact">contact page</a> to get in touch with our support team.</p>
            
            <p>Stay strong,</p>
            <p><strong>The Brawny Originals Team</strong></p>

            <p style="color: #666666; font-size: 12px; margin-top: 20px; padding-top: 10px; border-top: 1px solid #eeeeee;">
                <em>Please note: This is an automated message. Please do not reply to this email. For assistance, please visit our <a href="https://www.brawnyoriginals.com/#/contact" style="color: #1a1a1a;">contact page</a>.</em>
            </p>
        </div>
        
        <div class="footer">
            <p>© 2025 Brawny Originals. All rights reserved.</p>
        </div>
    </body>
    </html>
"""
