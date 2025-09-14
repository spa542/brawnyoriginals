import React from 'react';
import { Link } from 'react-router-dom';

const HomePage: React.FC = () => {
  return (
    <div className="w-full flex flex-col min-h-screen">
      {/* Hero Banner */}
      <div className="w-full bg-gray-100 flex-1 flex items-center">
        <div className="w-full max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12 md:py-24">
          <div className="text-center">
            <h1 className="text-5xl font-extrabold tracking-tight text-gray-900 sm:text-6xl lg:text-7xl">
              Brawny Originals
            </h1>
          </div>
        </div>
      </div>

      {/* Subheader Section */}
      <div className="bg-white w-full py-12 md:py-16 flex-shrink-0">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center">
            <p className="mt-6 max-w-2xl mx-auto text-xl text-gray-700">
              Professional training programs designed to help you achieve your fitness goals, no matter your starting point.
            </p>
            <div className="mt-10 flex flex-col sm:flex-row justify-center gap-4">
              <Link
                to="/programs"
                className="w-48 sm:w-56 inline-flex items-center justify-center px-6 py-4 border border-transparent text-base font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 md:text-lg transition-colors duration-200"
              >
                Explore Programs
              </Link>
              <Link
                to="/contact"
                className="w-48 sm:w-56 inline-flex items-center justify-center px-6 py-4 border border-gray-300 text-base font-medium rounded-md text-blue-700 bg-white hover:bg-gray-50 md:text-lg transition-colors duration-200"
              >
                Coaching
              </Link>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default HomePage;
