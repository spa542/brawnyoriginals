import React from 'react';
import { Link } from 'react-router-dom';

const BottomNavigation: React.FC = () => {
  return (
    <footer className="bg-primary text-secondary py-4 w-full">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex flex-col md:flex-row justify-between items-center">
          <div className="mb-3 md:mb-0">
            <Link to="/" className="flex items-center space-x-2">
              <span className="text-2xl font-pacifico text-secondary">Brawny Originals</span>
            </Link>
          </div>
          <nav className="flex flex-wrap justify-center gap-6">
            <Link 
              to="/" 
              className="text-secondary text-opacity-80 hover:text-opacity-100 transition-colors duration-200"
            >
              Home
            </Link>
            <Link 
              to="/programs" 
              className="text-secondary text-opacity-80 hover:text-opacity-100 transition-colors duration-200"
            >
              Programs
            </Link>
            <Link 
              to="/about" 
              className="text-secondary text-opacity-80 hover:text-opacity-100 transition-colors duration-200"
            >
              About
            </Link>
            <Link 
              to="/contact" 
              className="text-secondary text-opacity-80 hover:text-opacity-100 transition-colors duration-200"
            >
              Contact
            </Link>
          </nav>
        </div>
        <div className="mt-4 pt-4 text-center text-sm text-secondary text-opacity-60">
          © {new Date().getFullYear()} Brawny Originals. All rights reserved.
        </div>
      </div>
    </footer>
  );
};

export default BottomNavigation;
