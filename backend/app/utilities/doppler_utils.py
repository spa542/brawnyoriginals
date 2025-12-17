import os
import time
from typing import Dict, Optional
import httpx

import requests
from fastapi import HTTPException, status

from app.utilities.logger import get_logger
from app.utilities.helpers import get_cfg


class DopplerSecrets:
    """
    Singleton class to manage Doppler secrets with in-memory caching.
    Automatically refreshes secrets when the cache expires.
    """
    _instance: Optional['DopplerSecrets'] = None
    _secrets: Dict[str, str] = {}
    _last_fetch_time: float = 0
    _cache_ttl: int = 86400  # 24 hour TTL

    def __init__(self):
        if self._instance is not None:
            raise RuntimeError("Use get_doppler_client() instead")
        self._initialize()

    @classmethod
    def get_instance(cls) -> 'DopplerSecrets':
        """Get or create the singleton instance"""
        if cls._instance is None:
            cls._instance = cls.__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        self._logger = get_logger(__name__)
        self.doppler_api_key = os.getenv("DOPPLER_API_KEY")
        
        if not self.doppler_api_key:
            error_msg = "DOPPLER_API_KEY environment variable is not set"
            self._logger.error(error_msg)
            raise ValueError(error_msg)
        
        # Get config from config file
        cfg = get_cfg()
        
        try:
            self.project = cfg.get("DOPPLER", "project")
            self.config = cfg.get("DOPPLER", "config")
        except Exception as e:
            self._logger.error(f"Failed to load Doppler config: {str(e)}")
            raise ValueError("Invalid Doppler configuration in config file") from e
        
        self._logger.debug(f"Doppler client initialized - Project: {self.project}, Config: {self.config}")

    async def get_secret(self, secret_name: str) -> str:
        """
        Get a secret from Doppler with caching.
        
        Args:
            secret_name: Name of the secret to retrieve
            
        Returns:
            The secret value
            
        Raises:
            HTTPException: If secret is not found or there's an API error
        """
        current_time = time.time()
        
        # Refresh cache if TTL has expired or no secrets are loaded
        time_since_last_fetch = current_time - self._last_fetch_time
        if time_since_last_fetch > self._cache_ttl:
            self._logger.info(f"Cache TTL expired ({time_since_last_fetch:.1f}s > {self._cache_ttl}s). Refreshing secrets from Doppler...")
            await self._fetch_secrets()
        elif not self._secrets:
            self._logger.info("No secrets loaded. Fetching from Doppler...")
            await self._fetch_secrets()
        else:
            self._logger.info("Secrets already loaded. Using cached secrets.") 
        
        # Check if secret exists
        if secret_name not in self._secrets:
            self._logger.error(f"Secret '{secret_name}' not found in Doppler config")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Secret '{secret_name}' not found in Doppler config"
            )
            
        return self._secrets[secret_name]

    async def _fetch_secrets(self) -> None:
        """Fetch all secrets from Doppler API and update the cache"""
        url = "https://api.doppler.com/v3/configs/config/secrets/download"
        params = {
            "project": self.project,
            "config": self.config,
            "format": "json"
        }
        
        headers = {"Authorization": f"Bearer {self.doppler_api_key}"}
        
        try:
            self._logger.debug("Fetching secrets from Doppler")
            async with httpx.AsyncClient() as client:
                response = await client.get(url, params=params, headers=headers, timeout=15.0)
                response.raise_for_status()
                
                # Update cache
                self._secrets = response.json()
                self._last_fetch_time = time.time()
                self._logger.debug("Successfully updated secrets cache")
                
        except httpx.HTTPStatusError as e:
            self._logger.error(f"Failed to fetch secrets from Doppler: {str(e)}")
            # Don't clear existing cache if we fail to refresh
            if not self._secrets:
                raise HTTPException(
                    status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                    detail=f"Failed to fetch secrets from Doppler: {str(e)}"
                )
        except Exception as e:
            self._logger.error(f"Unexpected error fetching secrets: {str(e)}")
            if not self._secrets:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"Unexpected error fetching secrets: {str(e)}"
                )


async def get_doppler_secret(secret_name: str) -> str:
    """
    Get a secret from Doppler with caching.
    
    This is the main entry point for accessing secrets.
    
    Args:
        secret_name: The name of the secret to retrieve
        
    Returns:
        The secret value
        
    Example:
        >>> db_password = await get_doppler_secret("DB_PASSWORD")
    """
    client = DopplerSecrets.get_instance()
    return await client.get_secret(secret_name)
