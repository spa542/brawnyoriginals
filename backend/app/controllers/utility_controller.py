import os
import requests
from typing import Dict, Any

from app.utilities.helpers import is_dev
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
    # TODO: Update this based on environments using vault later
    if is_dev():
        uri = "https://api.mailgun.net/v3/sandbox643e4f56e5e64025bb465156f01fe8aa.mailgun.org/messages"
        email_from = "Mailgun Sandbox <postmaster@sandbox643e4f56e5e64025bb465156f01fe8aa.mailgun.org>"
        email_to = "ryan11291129@gmail.com"
    else:
        uri = "https://api.mailgun.net/v3/sandbox643e4f56e5e64025bb465156f01fe8aa.mailgun.org/messages" 
        email_from = "Mailgun Sandbox <postmaster@sandbox643e4f56e5e64025bb465156f01fe8aa.mailgun.org>"
        email_to = "ryan11291129@gmail.com"

    # TODO Update to use vault later
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
    response = requests.post(uri, auth=auth, data=data, timeout=10)
    response.raise_for_status()
    
    return SendEmailResponse(
        status="success",
        message="Email sent successfully"
    )
