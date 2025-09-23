import React from 'react';
import { Link } from 'react-router-dom';
import { getAssetPath } from '../utils/imageLoader';

const AboutPage: React.FC = () => {
  return (
    <div className="min-h-screen bg-secondary">
      {/* Hero Section */}
      <div className="bg-primary text-secondary py-20">
        <div className="container mx-auto px-4 text-center">
          <h1 className="text-4xl md:text-5xl font-bold mb-6">About Brawny Originals</h1>
          <p className="text-xl text-secondary text-opacity-90 max-w-3xl mx-auto">
            Dedicated to excellence in strength training and fitness
          </p>
        </div>
      </div>

      {/* Company Section */}
      <div className="py-16 bg-secondary">
        <div className="container mx-auto px-4">
          <div className="max-w-4xl mx-auto text-center">
            <div className="flex justify-center mb-10">
              <img 
                src={getAssetPath('images/brawny_originals_logo_white_no_bg.png')}
                alt="Brawny Originals Logo"
                className="h-40 w-auto"
                onError={(e) => {
                  console.error('Failed to load image:', (e.target as HTMLImageElement).src);
                  const target = e.target as HTMLImageElement;
                  target.src = '';
                }}
              />
            </div>
            <div className="prose prose-lg text-primary text-left">
              <p className="mb-6">
                [Company description will go here. This section should contain a detailed overview of Brawny Originals, 
                its mission, values, and history. The description should be engaging and informative, highlighting 
                what makes the company unique in the fitness industry.]
              </p>
              <p>
                [Additional details about the company's approach to training, philosophy, and commitment to clients 
                can be included here to provide a comprehensive understanding of the business.]
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* CTA Section - Removed extra padding and border */}
      <div className="bg-primary text-secondary pt-12 pb-16">
        <div className="container mx-auto px-4 text-center">
          <h2 className="text-3xl font-bold mb-6">Ready to Start Your Fitness Journey?</h2>
          <p className="text-xl text-secondary text-opacity-90 mb-8 max-w-2xl mx-auto">
            Join Brawny Originals today and experience the difference in your training.
          </p>
          <Link 
            to="/contact" 
            className="inline-block bg-tertiary-600 hover:bg-tertiary-700 text-secondary font-bold py-3 px-8 rounded-full transition-colors duration-300"
          >
            Contact Us
          </Link>
        </div>
      </div>
    </div>
  );
};

export default AboutPage;
