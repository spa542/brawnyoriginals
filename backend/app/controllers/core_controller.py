from typing import Dict, Any


def handle_404() -> Dict[str, Any]:
    """
    Handle 404 errors
    Returns:
        Dict with error details
    """
    return {
        "message": "Not Found"
    }


def handle_500() -> Dict[str, Any]:
    """
    Handle 500 errors
    Returns:
        Dict with error details
    """
    return {
        "message": "Internal Server Error"
    }
