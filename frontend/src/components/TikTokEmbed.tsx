import React from 'react';

interface TikTokEmbedProps {
  videoId: string;
  title: string;
  className?: string;
}

const TikTokEmbed: React.FC<TikTokEmbedProps> = ({
  videoId,
  title,
  className = '',
}) => {
  const embedUrl = `https://www.tiktok.com/embed/v2/${videoId}?lang=en-US`;
  
  return (
    <div className={`w-full ${className}`}>
      <div className="aspect-[9/16] w-full rounded-lg overflow-hidden shadow-lg">
        <iframe
          src={embedUrl}
          title={title}
          className="w-full h-full border-0 overflow-hidden"
          style={{
            overflow: 'hidden',
            margin: 0,
            padding: 0,
            display: 'block',
            maxHeight: '100%',
            maxWidth: '100%'
          }}
          allowFullScreen
          allow="accelerometer; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
        />
      </div>
    </div>
  );
};

export default TikTokEmbed;
