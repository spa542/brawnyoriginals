import React from 'react';
import Slider from 'react-slick';
import 'slick-carousel/slick/slick.css';
import 'slick-carousel/slick/slick-theme.css';
import { getAssetPath } from '../utils/imageLoader';

interface ImageCarouselProps {
  imageFilenames: string[];
}

interface CarouselImage {
  src: string;
  name: string;
}

const ImageCarousel: React.FC<ImageCarouselProps> = ({ imageFilenames }) => {
  // Convert filenames to image objects with src and name
  const images: CarouselImage[] = imageFilenames.map(filename => ({
    src: getAssetPath(`images/${filename}`),
    name: filename.replace(/\.[^/.]+$/, '').replace(/[-_]/g, ' ')
  }));

  // Slick carousel settings
  const settings = {
    dots: true,
    infinite: true,
    speed: 800,
    slidesToShow: 1,
    slidesToScroll: 1,
    autoplay: true,
    autoplaySpeed: 4000,
    pauseOnHover: false,
    pauseOnFocus: false,
    pauseOnDotsHover: false,
    fade: true,
    cssEase: 'ease-in-out',
    swipeToSlide: true,
    focusOnSelect: false,
    waitForAnimate: true,
    arrows: false,
    // Force reinitialization on window resize
    responsive: [
      {
        breakpoint: 1024,
        settings: {
          slidesToShow: 1,
          slidesToScroll: 1,
        }
      }
    ],
    appendDots: (dots: React.ReactNode) => (
      <div className="absolute bottom-4 w-full">
        <ul className="m-0 p-0 flex justify-center space-x-2">{dots}</ul>
      </div>
    ),
    customPaging: () => (
      <div className="w-3 h-3 rounded-full bg-white bg-opacity-50 hover:bg-opacity-100 transition-all duration-300"></div>
    ),
  };

  // Don't render anything if no images are available
  if (images.length === 0) {
    return null;
  }

  return (
    <div className="relative w-full">
      <div style={{ paddingBottom: '56.25%' }}> {/* 16:9 Aspect Ratio */}
        <div className="absolute inset-0">
          <Slider {...settings} className="h-full">
            {images.map((image, index) => (
              <div key={`${image.name}-${index}`} className="h-full">
                <div className="h-full w-full overflow-hidden">
                  <img 
                    src={image.src}
                    alt={image.name || `Gym photo ${index + 1}`}
                    className="w-full h-full object-cover rounded-lg"
                    onError={(e) => {
                      console.error('Failed to load image:', image.src);
                      const target = e.target as HTMLImageElement;
                      target.style.display = 'none';
                    }}
                    draggable={false}
                    loading="lazy"
                  />
                </div>
              </div>
            ))}
          </Slider>
        </div>
      </div>
    </div>
  );
};

export default ImageCarousel;
