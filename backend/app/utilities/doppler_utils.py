import os
import requests
from typing import Optional

from app.utilities.helpers import get_cfg
from app.utilities.logger import get_logger


# Module-level instance for singleton pattern
_instance = None


def _get_doppler_client(api_key: Optional[str] = None) -> 'DopplerClient':
    """
    Get the singleton instance of DopplerClient.
    
    Args:
        api_key: Optional API key. If not provided, will be read from environment.
                Only used on first call.
                
    Returns:
        DopplerClient: The singleton instance
    """
    global _instance
    if _instance is None:
        _instance = DopplerClient(api_key)
    return _instance


class DopplerClient:
    """
    Client for interacting with the Doppler API to fetch secrets.
    Should be instantiated through get_doppler_client().
    """
    
    BASE_URL = "https://api.doppler.com/v3"
    
    def __init__(self, api_key: Optional[str] = None) -> None:
        """
        Initialize the Doppler client with an optional API key.
        If no API key is provided, it will be read from the DOPPLER_API_KEY environment variable.
        
        Args:
            api_key: The Doppler API key. Defaults to None.
            
        Raises:
            ValueError: If no API key is provided and DOPPLER_API_KEY is not set.
        """
        self._logger = get_logger(__name__)
        self._logger.debug("Initializing Doppler client")
        
        self.api_key = api_key or os.getenv("DOPPLER_API_KEY")
        if not self.api_key:
            error_msg = "No API key provided and DOPPLER_API_KEY environment variable is not set"
            self._logger.error(error_msg)
            raise ValueError(error_msg)
        
        # Get project and config from the existing config system
        cfg = get_cfg()
        self.project = cfg.get("DOPPLER", "project", fallback=None)
        self.config = cfg.get("DOPPLER", "config", fallback=os.getenv("ENV", "dev"))
        
        self._logger.debug(
            "Doppler client initialized",
            extra={"project": self.project, "config": self.config}
        )
    
    def get_secret(self, secret_name: str) -> str:
        """
        Retrieve a secret from Doppler.
        
        Args:
            secret_name (str): The name of the secret to retrieve
            
        Returns:
            str: The secret value
            
        Raises:
            ValueError: If the project is not configured or secret is not found
            Exception: If the request to Doppler API fails
        """
        if not self.project:
            error_msg = "Doppler project not configured. Please set 'project' in the DOPPLER section of your config."
            self._logger.error(error_msg)
            raise ValueError(error_msg)
            
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Accept": "application/json"
        }
        
        url = f"{self.BASE_URL}/projects/{self.project}/configs/config/secrets?name={secret_name}"
        self._logger.debug("Fetching secret from Doppler", 
                         extra={"secret_name": secret_name, "project": self.project})
        
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            data = response.json()
            
            # The response structure may vary based on your Doppler setup
            if "secrets" in data and secret_name in data["secrets"]:
                secret_value = data["secrets"][secret_name]["value"]
                self._logger.debug("Successfully retrieved secret",
                                 extra={"secret_name": secret_name, "project": self.project})
                return secret_value
            elif "value" in data:
                self._logger.debug("Successfully retrieved secret (legacy format)",
                                 extra={"secret_name": secret_name, "project": self.project})
                return data["value"]
            else:
                error_msg = f"Secret '{secret_name}' not found in the response"
                self._logger.error(error_msg, extra={"response_data": data})
                raise ValueError(error_msg)
                
        except requests.exceptions.RequestException as e:
            error_msg = f"Failed to fetch secret from Doppler: {str(e)}"
            self._logger.exception(error_msg, extra={"secret_name": secret_name, "project": self.project})
            raise Exception(error_msg) from e


def get_doppler_secret(secret_name: str) -> str:
    """
    Convenience function to get a secret from Doppler using environment configuration.
    
    Args:
        secret_name: The name of the secret to retrieve
        
    Returns:
        The secret value
        
    Example:
        >>> db_password = get_doppler_secret("DB_PASSWORD")
    """
    client = _get_doppler_client()
    return client.get_secret(secret_name)
