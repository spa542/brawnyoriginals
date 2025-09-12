import React from 'react';
import { Link } from 'react-router-dom';

const HomePage: React.FC = () => {
  return (
    <div className="w-full flex flex-col">
      {/* Hero Banner */}
      <div className="w-full bg-gray-100">
        <div className="w-full py-16 md:py-20">
          <div className="text-center">
            <h1 className="text-4xl font-extrabold tracking-tight text-gray-900 sm:text-5xl lg:text-6xl">
              Transform Your Fitness Journey
            </h1>
            <p className="mt-6 max-w-2xl mx-auto text-xl text-gray-700">
              Professional training programs designed to help you achieve your fitness goals, no matter your starting point.
            </p>
            <div className="mt-10 flex flex-col sm:flex-row justify-center gap-3">
              <Link
                to="/programs"
                className="inline-flex items-center justify-center px-8 py-3 border border-transparent text-base font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 md:py-4 md:text-lg md:px-10 transition-colors duration-200"
              >
                Explore Programs
              </Link>
              <Link
                to="/contact"
                className="inline-flex items-center justify-center px-8 py-3 border border-transparent text-base font-medium rounded-md text-blue-700 bg-white hover:bg-gray-50 md:py-4 md:text-lg md:px-10 transition-colors duration-200"
              >
                Personal Training
              </Link>
            </div>
          </div>
        </div>
      </div>

      {/* Featured Programs */}
      <div className="bg-white w-full">
        <div className="w-full py-8">
          <div className="text-center">
            <h2 className="text-3xl font-extrabold text-gray-900 sm:text-4xl">
              Training Programs
            </h2>
            <p className="mt-4 max-w-2xl text-xl text-gray-500 mx-auto">
              Choose from our carefully designed programs to start your transformation today.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default HomePage;
