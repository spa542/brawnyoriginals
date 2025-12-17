import time
from typing import Dict, Optional, Any
import httpx

from fastapi import HTTPException, status
from app.utilities.logger import get_logger
from app.utilities.doppler_utils import get_doppler_secret


class YouTubeCache:
    """
    Singleton class to cache YouTube videos and shorts with TTL.
    """
    _instance: Optional['YouTubeCache'] = None
    _cache: Dict[str, Dict[str, Any]] = {
        'video': {'data': None, 'timestamp': 0},
        'short': {'data': None, 'timestamp': 0}
    }
    _ttl: int = 86400  # 24 hours in seconds

    def __new__(cls):
        if cls._instance is not None:
            raise RuntimeError("Use get_instance() instead")
        instance = super().__new__(cls)
        instance._logger = get_logger(__name__)
        return instance

    def __init__(self):
        # Skip initialization if already initialized
        if hasattr(self, '_initialized'):
            return
        self._initialized = True
        self._logger.info("Initializing YouTubeCache")

    @classmethod
    def get_instance(cls) -> 'YouTubeCache':
        """Get or create the singleton instance"""
        if cls._instance is None:
            cls._instance = cls()  # This will call both __new__ and __init__
        return cls._instance

    def get(self, cache_key: str) -> Optional[Dict]:
        """Get cached data if it exists and is not expired"""
        cache_entry = self._cache.get(cache_key)
        if not cache_entry or not cache_entry['data']:
            self._logger.info(f"Cache miss - No data for {cache_key}")
            return None

        current_time = time.time()
        time_since_update = current_time - cache_entry['timestamp']
        
        if time_since_update > self._ttl:
            self._logger.info(
                f"Cache expired for {cache_key} "
                f"(age: {time_since_update/3600:.1f}h > {self._ttl/3600:.1f}h)"
            )
            return None

        self._logger.info(
            f"Cache hit for {cache_key} "
            f"(age: {time_since_update/60:.1f}m)"
        )
        return cache_entry['data']

    def set(self, cache_key: str, data: Dict) -> None:
        """Store data in cache with current timestamp"""
        self._cache[cache_key] = {
            'data': data,
            'timestamp': time.time()
        }
        self._logger.info(f"Updated cache for {cache_key}")
        if cache_key in data.get('id', ''):
            self._logger.debug(f"Cached data: {data.get('id')}")
        else:
            self._logger.debug("Cached data updated")


# YouTube Caching mechanism
def get_youtube_cache() -> YouTubeCache:
    """Get the singleton instance of YouTubeCache with lazy initialization."""
    if YouTubeCache._instance is None:
        YouTubeCache._instance = YouTubeCache()
    return YouTubeCache._instance


# YouTube Data API v3 configuration
YOUTUBE_API_BASE_URL = "https://www.googleapis.com/youtube/v3"
CHANNEL_NAME = "brawnyoriginals"


async def get_channel_id(channel_name: str = CHANNEL_NAME) -> Optional[str]:
    """
    Get YouTube channel ID from channel name using YouTube Data API v3.
    
    Args:
        channel_name: The name of the YouTube channel
        
    Returns:
        Channel ID if found, None otherwise
        
    Raises:
        HTTPException: If there's an error with the YouTube API request
    """
    logger = get_logger(f"{__name__}.get_channel_id")
    logger.debug(f"Looking up channel ID for: {channel_name}")
    
    try:
        try:
            api_key = await get_doppler_secret("YOUTUBE_API_KEY")
        except Exception as e:
            logger.error(f"Failed to get YouTube API key from Doppler: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Server configuration error: Missing YouTube API key"
            )
            
        async with httpx.AsyncClient() as client:
            url = f"{YOUTUBE_API_BASE_URL}/search"
            params = {
                "part": "snippet",
                "q": channel_name,
                "type": "channel",
                "key": api_key,
                "maxResults": 1
            }
            
            logger.debug(f"Making request to: {url}")
            logger.debug(f"Request params: { {k: v for k, v in params.items() if k != 'key'} }")
            
            response = await client.get(url, params=params, timeout=15)
            
            # Log response status and headers for debugging
            logger.debug(f"Response status: {response.status_code}")
            logger.debug(f"Response headers: {dict(response.headers)}")
            
            response.raise_for_status()
            
            data = response.json()
            logger.debug(f"Response data: {data}")
            
            if data.get("items"):
                channel_id = data["items"][0]["snippet"]["channelId"]
                logger.debug(f"Found channel ID: {channel_id}")
                return channel_id
                
            logger.warning(f"No channel found for: {channel_name}")
            return None
            
    except httpx.HTTPStatusError as e:
        logger.error(f"Failed to fetch channel ID: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch channel information from YouTube"
        )
    except Exception as e:
        logger.error(f"Unexpected error getting channel ID: {str(e)}")
        raise


async def get_latest_videos(channel_id: str, is_short: bool = False) -> Optional[Dict]:
    """
    Get the latest video or short from a YouTube channel using YouTube Data API v3.
    
    Args:
        channel_id: YouTube channel ID
        is_short: Whether to filter for YouTube Shorts (videos < 60 seconds)
        
    Returns:
        Dictionary with video ID if found, None otherwise
        
    Raises:
        HTTPException: If there's an error with the YouTube API request
    """
    logger = get_logger(f"{__name__}.get_latest_videos")
    logger.debug(f"Fetching latest {'short' if is_short else 'video'} for channel: {channel_id}")
    
    try:
        api_key = await get_doppler_secret("YOUTUBE_API_KEY")
    except Exception as e:
        logger.error(f"Failed to get YouTube API key from Doppler: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Server configuration error: Missing YouTube API key"
        )
    
    try:
        async with httpx.AsyncClient() as client:
            # Get channel uploads playlist ID
            channel_response = await client.get(
                f"{YOUTUBE_API_BASE_URL}/channels",
                params={
                    "part": "contentDetails",
                    "id": channel_id,
                    "key": api_key
                },
                timeout=15
            )
            channel_response.raise_for_status()
            channel_data = channel_response.json()
            
            if not channel_data.get("items"):
                return None
                
            uploads_playlist_id = channel_data["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]
            
            # Get multiple recent videos from the uploads playlist
            videos_response = await client.get(
                f"{YOUTUBE_API_BASE_URL}/playlistItems",
                params={
                    "part": "contentDetails",
                    "playlistId": uploads_playlist_id,
                    "key": api_key,
                    "maxResults": 50  # Get enough videos to find both a short and regular video
                },
                timeout=15
            )
            videos_response.raise_for_status()
            videos_data = videos_response.json()
            
            if not videos_data.get("items"):
                return None
            
            # Get video IDs in batches of 50 (YouTube API limit)
            video_ids = [item["contentDetails"]["videoId"] for item in videos_data["items"]]
            
            # Get video details in a single batch request
            video_response = await client.get(
                f"{YOUTUBE_API_BASE_URL}/videos",
                params={
                    "part": "contentDetails,status",
                    "id": ",".join(video_ids),
                    "key": api_key
                },
                timeout=15
            )
            video_response.raise_for_status()
            video_details = video_response.json()
            
            if not video_details.get("items"):
                logger.warning("No video details found for any videos")
                return None
            
            # Process videos in order until we find the first matching video
            for video_info in video_details["items"]:
                # Skip unplayable videos
                if video_info.get("status", {}).get("privacyStatus") != "public":
                    continue
                    
                duration = video_info["contentDetails"]["duration"]
                video_id = video_info["id"]
                
                # Check if this is a short (less than 60 seconds)
                is_video_short = "M" not in duration and "H" not in duration and "S" in duration
                
                # If we found a video of the requested type, return it
                if is_short == is_video_short:
                    logger.debug(f"Found matching {'short' if is_short else 'regular'} video: {video_id}")
                    return {"id": video_id, "is_short": is_video_short}
            
            logger.debug(f"No {'short' if is_short else 'regular'} videos found in the first {len(video_ids)} videos")

            return None
    except Exception as e:
        logger.error(f"Unexpected error fetching videos: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while fetching videos"
        )


async def get_latest_video() -> Dict:
    """
    Get the latest regular video from the channel using cache or YouTube Data API v3.
    
    Returns:
        Dictionary containing video details
        
    Raises:
        HTTPException: If channel not found or no videos available
    """
    logger = get_logger(f"{__name__}.get_latest_video")
    logger.info("Fetching latest regular video")
    
    # Try to get from cache first
    cache = get_youtube_cache()
    cached_video = cache.get('video')
    if cached_video:
        logger.info("Returning cached video")
        return cached_video
    
    logger.info("Cache miss, fetching from YouTube API")
    channel_id = await get_channel_id()
    if not channel_id:
        logger.warning("YouTube channel not found")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="YouTube channel not found"
        )
    
    logger.debug(f"Found channel ID: {channel_id}, fetching latest video")
    video = await get_latest_videos(channel_id, is_short=False)
    
    if not video:
        logger.warning("No regular videos found for channel")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No videos found"
        )
    
    logger.debug(f"Found video with ID: {video.get('id')}")
    
    # Update cache
    cache = get_youtube_cache()
    cache.set('video', video)
    logger.info("Updated video cache")
    
    return video


async def get_latest_short() -> Dict:
    """
    Get the latest short from the channel using cache or YouTube Data API v3.
    
    Returns:
        Dictionary containing short video details
        
    Raises:
        HTTPException: If channel not found or no shorts available
    """
    logger = get_logger(f"{__name__}.get_latest_short")
    logger.info("Fetching latest short video")
    
    # Try to get from cache first
    cache = get_youtube_cache()
    cached_short = cache.get('short')
    if cached_short:
        logger.info("Returning cached short")
        return cached_short
    
    logger.info("Cache miss, fetching from YouTube API")
    channel_id = await get_channel_id()
    if not channel_id:
        logger.warning("YouTube channel not found")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="YouTube channel not found"
        )
    
    logger.debug(f"Found channel ID: {channel_id}, fetching latest short")
    video = await get_latest_videos(channel_id, is_short=True)
    
    if not video:
        logger.warning("No short videos found for channel")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No shorts found"
        )
    
    logger.debug(f"Found short with ID: {video.get('id')}")
    
    # Update cache
    cache = get_youtube_cache()
    cache.set('short', video)
    logger.info("Updated short video cache")
    
    return video
