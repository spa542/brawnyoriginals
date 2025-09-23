import React from 'react';
import { Link } from 'react-router-dom';
import ImageCarousel from '../components/ImageCarousel';


// List of filenames for the image carousel
const GALLERY_IMAGES = [
  'gym_photo_1.jpeg',
  'gym_photo_2.jpeg',
  'gym_photo_3.jpeg',
  'gym_photo_4.jpeg',
  'gym_photo_5.jpeg'
];


const HomePage: React.FC = () => {
  return (
    <div className="w-full flex flex-col min-h-screen">
      {/* Header with solid background */}
      <div className="w-full relative z-20 bg-secondary">
        <div className="relative">
          {/* Header content */}
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 md:py-12 text-center">
              <h1 className="text-4xl sm:text-5xl md:text-6xl lg:text-7xl font-extrabold text-primary">
              <span>Brawny Originals</span>
              </h1>
          </div>
        </div>
      </div>

      <div className="flex-1 flex flex-col">
        {/* Container for carousel with max width and auto margins */}
        <div className="w-full max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pt-4">
          <div className="w-full rounded-xl overflow-hidden shadow-2xl">
            <ImageCarousel imageFilenames={GALLERY_IMAGES} />
          </div>
        </div>

        {/* Subheader Section */}
        <div className="w-full bg-white pt-4 pb-12 md:pt-6 md:pb-16">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="text-center">
              <p className="mt-6 max-w-2xl mx-auto text-xl text-primary">
                Professional training programs and coaching designed to help you achieve your fitness goals, no matter your starting point.
              </p>
              <div className="mt-10 flex flex-col sm:flex-row justify-center gap-4">
                <Link
                  to="/programs"
                  className="w-48 sm:w-56 inline-flex items-center justify-center px-6 py-4 border border-primary text-base font-medium rounded-md text-secondary bg-tertiary-600 hover:bg-tertiary-700 md:text-lg transition-colors duration-200"
                >
                  Explore Programs
                </Link>
                <Link
                  to="/about"
                  className="w-48 sm:w-56 inline-flex items-center justify-center px-6 py-4 border border-primary text-base font-medium rounded-md text-secondary bg-tertiary-600 hover:bg-tertiary-700 md:text-lg transition-colors duration-200"
                >
                  About Us
                </Link>
                <Link
                  to="/contact"
                  className="w-48 sm:w-56 inline-flex items-center justify-center px-6 py-4 border border-primary text-base font-medium rounded-md text-secondary bg-tertiary-600 hover:bg-tertiary-700 md:text-lg transition-colors duration-200"
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
