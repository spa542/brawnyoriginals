import React, { useState } from 'react';

interface YouTubeEmbedProps {
  videoId: string;
  title: string;
  className?: string;
  isShort?: boolean;
}

const YouTubeEmbed: React.FC<YouTubeEmbedProps> = ({ 
  videoId, 
  title, 
  className = '',
  isShort = false
}) => {
  const [hasError, setHasError] = useState(false);
  const aspectRatio = isShort ? 'aspect-[9/16]' : 'aspect-video';
  
  const handleError = () => {
    setHasError(true);
  };

  if (hasError) {
    return (
      <div className={`w-full ${className}`}>
        <div className={`w-full ${aspectRatio} rounded-lg overflow-hidden shadow-lg bg-gray-100 flex items-center justify-center`}>
          <div className="text-center p-4">
            <p className="text-gray-700 font-medium">Couldn't load the video</p>
            <a 
              href={`https://youtube.com/watch?v=${videoId}`}
              target="_blank"
              rel="noopener noreferrer"
              className="text-blue-600 hover:underline mt-2 inline-block"
            >
              Watch on YouTube
            </a>
          </div>
        </div>
      </div>
    );
  }
  
  return (
    <div className={`w-full ${className}`}>
      <div className={`w-full ${aspectRatio} rounded-lg overflow-hidden shadow-lg`}>
        <iframe
          width="100%"
          height="100%"
          src={`https://www.youtube.com/embed/${videoId}?rel=0${isShort ? '&controls=0' : ''}`}
          title={title}
          onError={handleError}
          allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
          allowFullScreen
          className="w-full h-full"
          loading="lazy"
        />
      </div>
    </div>
  );
};

export default YouTubeEmbed;
