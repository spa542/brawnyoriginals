from fastapi import APIRouter, Request, status, HTTPException, BackgroundTasks
import stripe

from app.controllers import payments_controller
from app.models.payments_model import (
    CheckoutTokenRequest,
    CheckoutTokenResponse,
    CheckoutSessionResponse,
    WebhookResponse,
    CreateCheckoutSessionRequest
)
from app.utilities.logger import get_logger
from app.utilities.recaptcha import verify_recaptcha_token
from app.utilities.doppler_utils import get_doppler_secret


router = APIRouter()


@router.post(
    "/payments/generate-token",
    response_model=CheckoutTokenResponse,
    status_code=status.HTTP_200_OK,
    summary="Generate a checkout token",
    description="""Generates a secure HMAC token for creating a checkout session.
    
    This endpoint validates the CAPTCHA token and creates a time-limited HMAC token 
    that can be used to securely create a checkout session. The token includes all 
    necessary checkout parameters and is signed to prevent tampering.
    """
)
async def generate_token(
    token_request: CheckoutTokenRequest,
    request: Request
) -> CheckoutTokenResponse:
    """
    Generate a secure token for creating a checkout session.
    
    Args:
        token_request: The token generation request containing price IDs and CAPTCHA token
        request: The incoming request (used for IP-based rate limiting)
        
    Returns:
        CheckoutTokenResponse: Contains the generated token and its expiration time
        
    Raises:
        HTTPException: If CAPTCHA validation or token generation fails
    """
    logger = get_logger(__name__)
    
    try:
        # Verify reCAPTCHA token
        if not token_request.captcha_token:
            logger.warning("Missing CAPTCHA token")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="CAPTCHA token is required"
            )
            
        captcha_valid = await verify_recaptcha_token(token_request.captcha_token)
        
        if not captcha_valid:
            logger.warning("CAPTCHA validation failed", extra={"remote_ip": request.client.host if request.client else None})
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid or expired CAPTCHA token"
            )
            
        # Generate the checkout token
        response = await payments_controller.generate_checkout_token(token_request)
        
        logger.info(
            "Generated checkout token",
            extra={"price_ids": token_request.price_ids, "expires_at": response.expires_at}
        )
        return response
    except HTTPException as e:
        logger.warning(
            "Checkout token generation failed",
            extra={"status_code": e.status_code}
        )
        raise
    except Exception as e:
        logger.error(
            "Failed to generate checkout token",
            exc_info=True,
            extra={"price_ids": getattr(token_request, 'price_ids', [])}
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to generate checkout token"
        )


@router.post(
    "/payments/create-checkout-session",
    response_model=CheckoutSessionResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new checkout session",
    description="""Creates a new Stripe Checkout Session using a secure token and returns the session URL for redirection.
    
    This endpoint requires a valid token obtained from the /payments/generate-token endpoint.
    The token should be included in the request body along with the price_id and URLs.
    """
)
async def create_checkout_session(
    request: CreateCheckoutSessionRequest
) -> CheckoutSessionResponse:
    """
    Create a new checkout session for payment processing using a secure token.
    
    This endpoint creates a Stripe Checkout Session using a pre-authorized token
    and returns the URL to redirect the user to complete their payment.
    
    Args:
        request: The checkout session request data
        
    Returns:
        CheckoutSessionResponse: Contains the session ID and URL for redirection
        
    Raises:
        HTTPException: If the token is invalid, expired, or session creation fails
    """
    logger = get_logger(__name__)
    
    try:
        # Create the checkout session with the provided request data
        response = await payments_controller.create_checkout_session(
            token=request.token,
            price_ids=request.price_ids,
            quantity=request.quantity,
            success_url=str(request.success_url),
            cancel_url=str(request.cancel_url)
        )
        
        logger.info(
            "Created checkout session",
            extra={
                "session_id": response.session_id,
                "price_ids": request.price_ids,
                "quantity": request.quantity
            }
        )
        return response
    except HTTPException as e:
        logger.warning(
            "Checkout session creation processing failed",
            extra={"status_code": e.status_code}
        )
        raise
    except Exception as e:
        logger.error(
            "Failed to create checkout session",
            exc_info=True,
            extra={"error": str(e)}
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create checkout session"
        )


# TODO: Add background tasks here to handle and fulfill orders quickly while returnign a quick response
@router.post(
    "/payments/stripe/webhook",
    response_model=WebhookResponse,
    status_code=status.HTTP_200_OK,
    include_in_schema=False,  # Exclude from OpenAPI schema as it's a webhook
    summary="Stripe webhook handler",
    description="Handles incoming webhook events from Stripe asynchronously."
)
async def webhook_handler(background_tasks: BackgroundTasks, request: Request) -> WebhookResponse:
    """
    Handle incoming webhook events from Stripe asynchronously.
    
    This endpoint quickly acknowledges receipt of webhook events from Stripe
    and processes them in the background to ensure timely responses.
    
    Args:
        background_tasks: FastAPI's BackgroundTasks for async processing
        request: The incoming HTTP request containing the webhook event
        
    Returns:
        WebhookResponse: Immediate acknowledgment of received webhook
        
    Raises:
        HTTPException: If the webhook signature is invalid
    """
    logger = get_logger(__name__)
    
    try:
        # Verify the webhook signature first (synchronous part)
        payload = await request.body()
        sig_header = request.headers.get('stripe-signature')
        webhook_secret = await get_doppler_secret("STRIPE_WEBHOOK_SECRET_KEY")
        
        try:
            event = stripe.Webhook.construct_event(payload, sig_header, webhook_secret)
            # Store the event for future processing in the background task
            request.state.event = event
        except ValueError as e:
            logger.warning("Invalid Stripe webhook payload", exc_info=True)
            raise HTTPException(status_code=400, detail="Invalid payload") from e
        except stripe.error.SignatureVerificationError as e:
            logger.warning("Invalid Stripe signature", exc_info=True)
            raise HTTPException(status_code=400, detail="Invalid signature") from e
        
        # Queue the webhook processing in the background
        background_tasks.add_task(payments_controller.handle_webhook, request)
        
        # Return immediate response
        return WebhookResponse(
            received=True,
            event_type=event.type,
            event_id=event.id
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Unexpected error in webhook handler", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        ) from e
    except Exception as e:
        logger.error(
            "Webhook processing error",
            exc_info=True
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to process webhook"
        )
