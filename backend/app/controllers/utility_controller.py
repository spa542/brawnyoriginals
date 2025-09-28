import os
import requests
from typing import Dict, Any

from app.utilities.helpers import is_dev, get_cfg
from app.models.utility_model import SendEmailResponse


def send_email(name: str, email: str, message: str) -> Dict[str, Any]:
    """
    Send email to the specified email address.
    
    Args:
        name: Name of the sender
        email: Email address of the sender
        message: Email message content
        
    Returns:
        Dict containing status and message
        
    Raises:
        ValueError: If there's an error sending the email
    """
    # Get config file
    cfg = get_cfg()
    # Setup email variables
    url = cfg.get("MAILGUN", "url")
    email_from = ("Mailgun Sandbox" if is_dev() else "Mailgun Production") + f" <{cfg.get('MAILGUN', 'from_uri')}>"
    email_to = cfg.get("MAILGUN", "contact_email")

    # TODO Update to use doppler later
    auth = ("api", os.getenv("MAILGUN_API_KEY"))
    if not auth[1]:
        raise ValueError("MAILGUN_API_KEY not found")
    # TODO Adjust email message based on type of email being sent
    data = {
        "from": email_from,
        "to": email_to,
        "subject": f"Brawny Originals - Contact Form - Message from {name} <{email}>",
        "text": message
    }

    # Send the email
    response = requests.post(url, auth=auth, data=data, timeout=10)
    response.raise_for_status()
    
    return SendEmailResponse(
        status="success",
        message="Email sent successfully"
    )
