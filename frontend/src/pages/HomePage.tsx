import React from 'react';
import { Link } from 'react-router-dom';
import ImageCarousel from '../components/ImageCarousel';


// List of filenames for the image carousel
const GALLERY_IMAGES = [
  'gym_photo_1_high_res.jpeg',
  'gym_photo_2_high_res.jpeg',
  'gym_photo_3_high_res.jpeg',
  'gym_photo_4_high_res.jpeg',
  'gym_photo_5_high_res.jpeg',
  'gym_photo_6_high_res.jpeg'
];


const HomePage: React.FC = () => {
  return (
    <div className="w-full flex flex-col min-h-screen bg-primary">
      <div className="relative w-full flex-grow">
        {/* Full viewport height carousel */}
        <div className="relative w-full h-full">
          <div className="w-full h-full bg-primary">
            <ImageCarousel imageFilenames={GALLERY_IMAGES} />
            {/* Centered title - Moved up */}
            {/* Dark overlay for better text contrast */}
            <div className="absolute inset-0 bg-black bg-opacity-30 z-0" />
            <div className="absolute inset-0 flex items-center justify-center z-10 pointer-events-none px-4" style={{ transform: 'translateY(-25%)' }}>
              <div className="w-full max-w-4xl mx-auto px-4 sm:px-6 py-6 sm:py-8 bg-black bg-opacity-40 rounded-lg backdrop-blur-sm">
                <h1 className="text-3xl sm:text-5xl md:text-6xl lg:text-7xl font-extrabold text-white text-center">
                  Brawny Originals
                </h1>
              </div>
            </div>
          </div>
        </div>

        {/* Subheader Section - Overlaying carousel */}
        <div className="absolute bottom-1/4 left-0 right-0 z-20 w-full px-4">
          <div className="max-w-4xl mx-auto px-4 sm:px-6 py-4 sm:py-6 bg-black bg-opacity-40 rounded-lg backdrop-blur-sm">
            <div className="text-center">
              <p className="text-base sm:text-lg md:text-xl text-white px-2">
                Professional training programs and coaching designed to help you achieve your fitness goals, no matter your starting point.
              </p>
              <div className="mt-4 sm:mt-6 flex flex-col sm:flex-row justify-center items-center gap-3 sm:gap-4">
                <Link
                  to="/programs"
                  className="w-full sm:w-48 md:w-56 inline-flex items-center justify-center px-4 sm:px-6 py-3 sm:py-4 border border-primary text-sm sm:text-base font-medium rounded-md text-secondary bg-tertiary-600 hover:bg-tertiary-700 md:text-lg transition-colors duration-200"
                >
                  Explore Programs
                </Link>
                <Link
                  to="/about"
                  className="w-full sm:w-48 md:w-56 inline-flex items-center justify-center px-4 sm:px-6 py-3 sm:py-4 border border-primary text-sm sm:text-base font-medium rounded-md text-secondary bg-tertiary-600 hover:bg-tertiary-700 md:text-lg transition-colors duration-200"
                >
                  About Us
                </Link>
                <Link
                  to="/contact"
                  className="w-full sm:w-48 md:w-56 inline-flex items-center justify-center px-4 sm:px-6 py-3 sm:py-4 border border-primary text-sm sm:text-base font-medium rounded-md text-secondary bg-tertiary-600 hover:bg-tertiary-700 md:text-lg transition-colors duration-200"
                >
                  Coaching
                </Link>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default HomePage;
