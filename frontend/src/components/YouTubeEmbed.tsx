import React from 'react';

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
  const aspectRatio = isShort ? 'aspect-[9/16]' : 'aspect-video';
  
  return (
    <div className={`w-full ${className}`}>
      <div className={`w-full ${aspectRatio} rounded-lg overflow-hidden shadow-lg`}>
        <iframe
          width="100%"
          height="100%"
          src={`https://www.youtube.com/embed/${videoId}${isShort ? '?controls=0' : ''}`}
          title={title}
          allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
          allowFullScreen
          className="w-full h-full"
        />
      </div>
    </div>
  );
};

export default YouTubeEmbed;
