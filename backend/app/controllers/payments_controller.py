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


async def handle_webhook(request: Request) -> None:
    """
    Process a Stripe webhook event in the background.
    
    This function processes the webhook event that has already been verified
    by the router. The event object is expected to be stored in request.state.
    
    Args:
        request: The incoming webhook request with the Stripe event in request.state.event
    """
    logger = get_logger(__name__)
    
    try:
        # Get the event from request state (already verified in the router)
        event = request.state.event
        
        logger.info(
            "Processing webhook event in background",
            extra={
                "event_id": event.id,
                "event_type": event.type,
                "livemode": event.livemode
            }
        )
        
        # Handle the event based on its type
        if event.type == 'payment_intent.succeeded':
            # Fulfill the order!
            payment_intent = event.data.object
            logger.info(
                "Payment intent succeeded",
                extra={
                    "payment_intent_id": payment_intent.id,
                    "amount_received": getattr(payment_intent, 'amount_received', None),
                    "currency": getattr(payment_intent, 'currency', None),
                    "customer_id": getattr(payment_intent, 'customer', None),
                    "payment_method": getattr(payment_intent, 'payment_method', None),
                    "metadata": dict(getattr(payment_intent, 'metadata', {})),
                    "charges": {
                        'count': len(getattr(payment_intent, 'charges', {}).get('data', [])),
                        'amounts': [c.get('amount') for c in getattr(payment_intent, 'charges', {}).get('data', []) if 'amount' in c]
                    } if hasattr(payment_intent, 'charges') else None
                }
            )
            await handle_payment_intent_succeeded(payment_intent)
            
        elif event.type == 'checkout.session.completed':
            # Log completed checkout session for bookkeeping
            session = event.data.object
            logger.info(
                "Checkout session completed",
                extra={
                    "session_id": session.id,
                    "customer_email": getattr(session, 'customer_email', None),
                    "payment_intent": getattr(session, 'payment_intent', None),
                    "amount_total": getattr(session, 'amount_total', None),
                    "currency": getattr(session, 'currency', None)
                }
            )
            
        elif event.type == 'checkout.session.expired':
            # Log expired checkout session for bookkeeping
            session = event.data.object
            logger.info(
                "Checkout session expired",
                extra={
                    "session_id": session.id,
                    "customer_email": getattr(session, 'customer_email', None),
                    "expires_at": getattr(session, 'expires_at', None)
                }
            )
            
        elif event.type == 'payment_intent.payment_failed':
            # Log failed payment for bookkeeping
            payment_intent = event.data.object
            logger.warning(
                "Payment failed",
                extra={
                    "payment_intent_id": payment_intent.id,
                    "amount": getattr(payment_intent, 'amount', None),
                    "currency": getattr(payment_intent, 'currency', None),
                    "failure_code": getattr(payment_intent, 'last_payment_error', {})
                                    .get('code', None) if hasattr(payment_intent, 'last_payment_error') else None,
                    "failure_message": getattr(payment_intent, 'last_payment_error', {})
                                    .get('message', None) if hasattr(payment_intent, 'last_payment_error') else None
                }
            )
        else:
            logger.debug(
                "Received unhandled event type",
                extra={"event_type": event.type}
            )
            
    except Exception as e:
        logger.error(
            "Error processing webhook event",
            extra={
                "event_type": getattr(event, 'type', 'unknown'),
                "event_id": getattr(event, 'id', 'unknown'),
                "error": str(e),
                "error_type": type(e).__name__
            },
            exc_info=True
        )


async def handle_payment_intent_succeeded(payment_intent: stripe.PaymentIntent) -> None:
    """Handle successful payment intent."""
    logger = get_logger(__name__)
    try:
        # TODO UPDATE LOGGING HERE 
        logger.info(
            "Payment intent succeeded",
            extra={
                "payment_intent_id": payment_intent.id,
                "amount": payment_intent.amount,
                "currency": payment_intent.currency,
                "customer": payment_intent.customer
            }
        )
        
        # TODO: Add your business logic here
        # Example: Update order status, fulfill order, etc.
        
    except Exception as e:
        logger.error(
            "Error handling payment_intent.succeeded",
            extra={"payment_intent_id": payment_intent.id},
            exc_info=True
        )
        raise
