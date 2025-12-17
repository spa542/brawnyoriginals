"""
Rate limiter configuration for the application.
"""
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded


# Initialize the rate limiter
limiter = Limiter(key_func=get_remote_address)

# Export the rate limit exceeded handler
export_rate_limit_exceeded_handler = _rate_limit_exceeded_handler
export_RateLimitExceeded = RateLimitExceeded
