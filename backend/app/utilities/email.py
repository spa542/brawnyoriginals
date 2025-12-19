from typing import Dict, List, Optional, Literal
import logging

from fastapi import UploadFile
import requests

from app.utilities.helpers import is_dev, get_cfg
from app.utilities.doppler_utils import get_doppler_secret
from app.models.payments_model import PdfAttachment


async def send_email_util(
    name: str,
    email: str,
    message: str,
    mode: Literal['contact','fulfillment'],
    files: Optional[List[PdfAttachment]] = None,
    is_html: bool = False
) -> Dict[str, str]:
    """
    Core email sending functionality with support for file attachments and HTML content.
    
    Args:
        name: Name of the sender
        email: Email address of the sender
        message: Email message content (can be plain text or HTML)
        mode: Either 'contact' or 'fulfillment' to determine the recipient and subject
        files: Optional list of files to attach to the email
        is_html: If True, the message will be sent as HTML content. Defaults to False.
        
    Returns:
        Dict containing status and message
        
    Raises:
        EmailConfigurationError: If there's an error with the email configuration
        requests.exceptions.RequestException: If there's an error sending the email
        Exception: For any other unexpected errors
    """
    logger = logging.getLogger(__name__)

    # Get Config 
    cfg = get_cfg()

    # Setup email variables
    url = cfg.get("MAILGUN", "url")
    email_to = cfg.get("MAILGUN", "contact_email") if mode == "contact" else email

    # Determine variables based on mode
    if mode == "contact":
        email_prefix = "Mailgun Sandbox" if is_dev() else "Mailgun Production"
        email_subject = f"Brawny Originals - Contact Form - Message from {name} <{email}>"
    else: # fulfillment 
        email_prefix = "Brawny Originals"
        email_subject = "Brawny Originals - Fulfillment Request - Order Details - DO NOT REPLY"

    email_from = f"{email_prefix} <{cfg.get('MAILGUN', 'from_uri')}>"

    try:
        mailgun_api_key = await get_doppler_secret("MAILGUN_API_KEY")
        if not mailgun_api_key:
            logger.error("Mailgun API key is not configured")
            raise ValueError("Email service configuration is incomplete")
        auth = ("api", mailgun_api_key)
    except Exception as e:
        logger.error(f"Failed to get Mailgun API key from Doppler: {str(e)}")
        raise RuntimeError("Failed to initialize email service") from e
        
    try:
        # Prepare email data
        data = {
            "from": email_from,
            "to": email_to,
            "subject": email_subject,
        }
        
        # Add message as either text or HTML based on flag
        if is_html:
            data["html"] = message
        else:
            data["text"] = message
        
        logger.debug(f"Sending email to: {email_to}, Subject: {email_subject}")
        
        # Prepare files if any
        files_data = []
        if files:
            for file in files:
                files_data.append(("attachment", (file.filename, file.content, file.content_type)))
        
        # Send the email with or without attachments
        if files_data:
            response = requests.post(
                url,
                auth=auth,
                data=data,
                files=files_data,
                timeout=30  # Increased timeout for file uploads
            )
        else:
            response = requests.post(
                url,
                auth=auth,
                data=data,
                timeout=10
            )
            
        response.raise_for_status()
        
        logger.info(f"Email sent successfully to: {email_to}, From: {email}")
        
        return {
            "status": "success",
            "message": "Email sent successfully"
        }
        
    except requests.exceptions.Timeout as e:
        error_msg = f"Email sending timed out after {e.request.timeout} seconds"
        logger.error(f"{error_msg} - From: {email}, To: {email_to}")
        raise TimeoutError("Email sending timed out. Please try again later.") from e
    except requests.exceptions.HTTPError as e:
        error_msg = f"Email service returned error: {e.response.status_code} - {e.response.text}"
        logger.error(f"{error_msg} - From: {email}, To: {email_to}, Status Code: {e.response.status_code}")
        raise ConnectionError("Failed to send email due to a service error") from e
    except requests.exceptions.RequestException as e:
        error_msg = f"Failed to send email: {str(e)}"
        logger.error(f"{error_msg} - From: {email}, To: {email_to}")
        raise ConnectionError("Failed to connect to email service") from e
    except Exception as e:
        error_msg = f"Unexpected error while sending email: {str(e)}"
        logger.error(f"{error_msg} - From: {email}, To: {email_to}")
        raise RuntimeError("An error occurred while sending the email") from e
