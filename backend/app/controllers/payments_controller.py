from typing import Dict, List
from fastapi import HTTPException, status, Request

import stripe

from app.models.payments_model import (
    CheckoutSessionResponse,
    WebhookResponse,
    CheckoutTokenRequest,
    CheckoutTokenResponse,
    CheckoutTokenData
)
from app.utilities.logger import get_logger
from app.utilities.doppler_utils import get_doppler_secret
from app.utilities.hmac import generate_hmac_token, verify_hmac_token
from app.utilities.helpers import get_cfg


# Configure Stripe with secret from Doppler and version from config
async def get_stripe_client():
    """
    Get configured Stripe client with API key from Doppler and version from config.
    
    Returns:
        stripe: Configured Stripe client
        
    Raises:
        HTTPException: If Stripe client initialization fails
    """
    logger = get_logger(__name__)
    
    try:
        # Get API key from Doppler
        stripe.api_key = await get_doppler_secret("STRIPE_SECRET_KEY")
        
        # Get API version from config file
        cfg = get_cfg()
        stripe.api_version = cfg.get('STRIPE', 'api_version')
        
        logger.debug("Initialized Stripe client", 
                    extra={"api_version": stripe.api_version})
        return stripe
    except Exception as e:
        logger.error("Failed to initialize Stripe client", 
                    exc_info=True,
                    extra={"error": str(e)})
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to initialize payment processor"
        ) from e


async def get_token_data(token: str) -> CheckoutTokenData:
    """
    Get and validate token data from an HMAC token.
    
    Args:
        token: The HMAC token
        
    Returns:
        CheckoutTokenData: The validated token data
        
    Raises:
        HTTPException: If token validation fails
    """
    logger = get_logger(__name__)
    
    try:
        token_dict = await verify_hmac_token(token)
        token_data = CheckoutTokenData(**token_dict)
        
        if token_data.is_expired():
            logger.warning("Token validation failed: token expired")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token has expired"
            )
        
        return token_data
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Token validation failed: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        ) from e


async def generate_checkout_token(
    token_request: CheckoutTokenRequest
) -> CheckoutTokenResponse:
    """
    Generate a secure token for creating a checkout session.
    
    Args:
        token_request: Token generation request data
        
    Returns:
        CheckoutTokenResponse containing the token and expiration
        
    Raises:
        HTTPException: If there's an error generating the token
    """
    logger = get_logger(__name__)
    
    try:
        # Create token data with expiration
        token_data = CheckoutTokenData.from_request(token_request)
        
        # Generate HMAC token
        token = await generate_hmac_token(token_data.model_dump())
        
        logger.info("Generated checkout token", extra={"expires_at": token_data.expires_at})
        
        return CheckoutTokenResponse(
            token=token,
            expires_at=token_data.expires_at
        )
        
    except Exception as e:
        logger.error("Error generating checkout token", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error generating checkout token"
        ) from e


async def create_checkout_session(
    token: str,
    price_ids: List[str],
    quantity: int = 1,
    success_url: str = None,
    cancel_url: str = None
) -> CheckoutSessionResponse:
    """
    Create a Stripe Checkout Session using a secure token
    
    Args:
        token: HMAC token from /payments/generate-token
        price_ids: List of Stripe price IDs for the products
        quantity: Number of items to purchase (default: 1)
        success_url: URL to redirect after successful payment
        cancel_url: URL to redirect if payment is cancelled
        
    Returns:
        CheckoutSessionResponse with session details
        
    Raises:
        HTTPException: If there's an error creating the checkout session
    """
    logger = get_logger(__name__)
    
    try:
        # Validate the token (this will raise an exception if invalid)
        token_data = await get_token_data(token)
        
        # Get the configured Stripe client
        stripe = await get_stripe_client()
        
        # Get the price_ids from the token data 
        price_ids = token_data.price_ids
            
        logger.info(
            "Creating checkout session",
            extra={
                "price_ids": price_ids,
                "quantity": quantity,
                "success_url": success_url,
                "cancel_url": cancel_url
            }
        )
        
        # Create line items for each price ID
        line_items = [{
            'price': price_id,
            'quantity': quantity,
        } for price_id in price_ids]
        
        # Get payment method configuration ID from config
        cfg = get_cfg()
        payment_method_config_id = cfg.get('STRIPE', 'payment_method_configuration_id')
        
        # Create a new checkout session with Stripe
        session_params = {
            'line_items': line_items,
            'mode': 'payment',
            'success_url': str(success_url),
            'cancel_url': str(cancel_url),
            'payment_method_configuration': payment_method_config_id
        }
        
        # Create the Stripe checkout session
        session = stripe.checkout.Session.create(**session_params)
        
        logger.info("Created checkout session", extra={"session_id": session.id})
        
        return CheckoutSessionResponse(
            session_id=session.id,
            url=session.url,
            expires_at=int(session.expires_at),
            payment_status=session.payment_status
        )
        
    except HTTPException:
        raise
    except stripe.error.StripeError as e:
        logger.error("Stripe API error", exc_info=True, extra={"error": str(e)})
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error("Error creating checkout session", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while creating the checkout session"
        ) from e


async def fulfill_order(session_id: str) -> Dict[str, str]:
    """
    Fulfill the customer's order after payment
    
    Args:
        session_id: The Stripe Checkout Session ID
        
    Returns:
        Dict with fulfillment status
        
    Raises:
        HTTPException: If there's an error during order fulfillment
        
    Note:
        This is a placeholder for order fulfillment logic
    """
    logger = get_logger(__name__)
    
    try:
        # Get Stripe client
        stripe_client = await get_stripe_client()
        
        # Retrieve the session to get the latest information
        session = stripe_client.checkout.Session.retrieve(session_id)
        
        # Log the fulfillment start
        logger.info(
            "Order fulfillment started",
            extra={
                "session_id": session_id,
                "payment_status": session.payment_status,
                "customer_email": session.customer_details.email if hasattr(session.customer_details, 'email') else None
            }
        )
        
        # TODO: Implement actual order fulfillment logic here
        # This could include:
        # 1. Updating your database
        # 2. Sending confirmation emails
        # 3. Triggering shipping processes
        # 4. Updating inventory
        
        logger.info("Order fulfillment completed", extra={"session_id": session_id})
        
        return {"status": "success", "message": "Order is being processed"}
        
    except HTTPException:
        raise
    except stripe.error.StripeError as e:
        logger.error("Stripe error during order fulfillment", exc_info=True, extra={"session_id": session_id})
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        ) from e
    except Exception as e:
        logger.error("Error during order fulfillment", exc_info=True, extra={"session_id": session_id})
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while processing your order"
        ) from e


async def handle_webhook(request: Request) -> WebhookResponse:
    """
    Handle Stripe webhook events
    
    Args:
        request: The incoming request with the webhook event
        
    Returns:
        WebhookResponse with event details
        
    Raises:
        HTTPException: If the webhook signature is invalid or event processing fails
    """
    logger = get_logger(__name__)
    payload = await request.body()
    sig_header = request.headers.get('stripe-signature')
    
    if not sig_header:
        logger.warning("Missing Stripe-Signature header")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Missing Stripe-Signature header"
        )
    
    try:
        # Get webhook secret from Doppler
        webhook_secret = await get_doppler_secret("STRIPE_WEBHOOK_SECRET")
        
        # Verify webhook signature
        event = stripe.Webhook.construct_event(
            payload, sig_header, webhook_secret
        )
        
        logger.info(
            "Received webhook event",
            extra={"event_id": event.id, "event_type": event.type}
        )
        
        # Handle the event
        if event.type == 'checkout.session.completed':
            session = event.data.object  # contains a stripe.PaymentIntent
            logger.info("Checkout session completed", extra={"session_id": session.id})
            # TODO: Handle successful payment
            
        elif event.type == 'payment_intent.succeeded':
            payment_intent = event.data.object  # contains a stripe.PaymentIntent
            logger.info("Payment succeeded", extra={"payment_intent_id": payment_intent.id})
            # TODO: Handle successful payment
            
        elif event.type == 'payment_intent.payment_failed':
            payment_intent = event.data.object
            logger.warning("Payment failed", extra={"payment_intent_id": payment_intent.id})
            # TODO: Handle failed payment
        
        return WebhookResponse(
            received=True,
            event_type=event.type,
            event_id=event.id
        )
        
    except stripe.error.SignatureVerificationError as e:
        logger.error("Invalid webhook signature", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid webhook signature"
        )
    except Exception as e:
        logger.error("Error processing webhook", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error processing webhook"
        )
