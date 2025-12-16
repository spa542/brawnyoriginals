import React, { useEffect, useState } from 'react';
import LoadingSpinner from './LoadingSpinner';
import { getBaseUrl } from '../utils/helpers';

type VideoType = 'youtube' | 'short' | 'tiktok';

interface VideoLoaderProps {
  type: VideoType;
  children: (props: { videoId: string }) => React.ReactNode;
}

const VideoLoader: React.FC<VideoLoaderProps> = ({ type, children }) => {
  const [videoId, setVideoId] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const fetchVideo = async () => {
      try {
        setIsLoading(true);
        setError(null);
        
        const baseUrl = getBaseUrl();
        const endpoint = 
          type === 'youtube' ? `${baseUrl}/api/latest/youtube` :
          type === 'short' ? `${baseUrl}/api/latest/short` :
          `${baseUrl}/api/latest/tiktok`;
        
        const response = await fetch(endpoint);
        
        if (!response.ok) {
          throw new Error(`Failed to fetch ${type} video`);
        }
        
        const data = await response.json();
        if (!data.video_id) {
          throw new Error('No video ID returned');
        }
        setVideoId(data.video_id);
      } catch (error) {
        console.error(`Error fetching ${type} video:`, error);
        setVideoId(null);
        setError('Video not available');
      } finally {
        setIsLoading(false);
      }
    };

    fetchVideo();
  }, [type]);

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-64 bg-gray-100 rounded-lg">
        <LoadingSpinner size="lg" />
      </div>
    );
  }

  if (error || !videoId) {
    return (
      <div className="flex items-center justify-center h-64 bg-gray-100 rounded-lg">
        <p className="text-primary">Video not available</p>
      </div>
    );
  }

  return <>{children({ videoId })}</>;
};

export default VideoLoader;
