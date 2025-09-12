import React from 'react';
import { Link } from 'react-router-dom';

const BottomNavigation: React.FC = () => {
  return (
    <footer className="bg-black text-white py-4 w-full">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex flex-col md:flex-row justify-between items-center">
          <div className="mb-4 md:mb-0">
            <span className="text-2xl font-pacifico">Brawny Originals</span>
          </div>
          <nav className="flex flex-wrap justify-center gap-6">
            <Link 
              to="/" 
              className="text-gray-300 hover:text-white transition-colors duration-200"
            >
              Home
            </Link>
            <Link 
              to="/programs" 
              className="text-gray-300 hover:text-white transition-colors duration-200"
            >
              Programs
            </Link>
            <Link 
              to="/contact" 
              className="text-gray-300 hover:text-white transition-colors duration-200"
            >
              Contact
            </Link>
          </nav>
        </div>
        <div className="mt-4 text-center text-sm text-gray-400">
          © {new Date().getFullYear()} Brawny Originals. All rights reserved.
        </div>
      </div>
    </footer>
  );
};

export default BottomNavigation;
