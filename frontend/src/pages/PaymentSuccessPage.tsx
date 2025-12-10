import React from 'react';
import { useNavigate } from 'react-router-dom';
import { MdCheckCircle } from 'react-icons/md';

const PaymentSuccessPage: React.FC = () => {
  const navigate = useNavigate();

  const scrollToDetails = () => {
    const element = document.getElementById('order-details');
    if (element) {
      element.scrollIntoView({ behavior: 'smooth' });
    }
  };

  const navigateToTop = (path: string) => {
    navigate(path);
    window.scrollTo(0, 0);
  };

  return (
    <div className="min-h-screen bg-secondary">
      {/* Hero Section */}
      <div className="bg-primary text-secondary flex-grow flex items-center justify-center py-20">
        <div className="container mx-auto px-4 text-center">
          <div className="flex justify-center mb-6">
            <MdCheckCircle className="w-28 h-28 md:w-40 md:h-40 text-green-500" />
          </div>
          <h1 className="text-3xl md:text-4xl lg:text-5xl font-bold mb-6">
            Payment Successful!
          </h1>
          <p className="text-sm md:text-base text-secondary text-opacity-90 max-w-3xl mx-auto mb-8">
            Thank you for your purchase. Your transaction has been completed successfully.
          </p>
          <div className="flex justify-center">
            <button onClick={scrollToDetails} className="flex flex-row items-center gap-3 text-secondary hover:text-tertiary-400 transition-colors cursor-pointer">
              <span className="text-base md:text-lg font-semibold">View Full Order Details</span>
              <svg className="w-6 h-6 animate-bounce" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 14l-7 7m0 0l-7-7m7 7V3" />
              </svg>
            </button>
          </div>
        </div>
      </div>

      {/* Details Section */}
      <div className="py-16 md:py-24 bg-secondary" id="order-details">
        <div className="container mx-auto px-4">
          <div className="max-w-2xl mx-auto text-left border border-primary-200 p-6 rounded-lg">
            <h2 className="text-2xl md:text-3xl font-bold text-primary mb-8">Order Details</h2>
            <div className="space-y-6">
              <div className="border-b border-primary-200 pb-6">
                <p className="text-primary text-opacity-90 mb-2">
                  <span className="font-semibold text-lg">Order Status</span>
                </p>
                <p className="text-primary text-opacity-80 text-lg">Confirmed</p>
              </div>
              <div className="border-b border-primary-200 pb-6">
                <p className="text-primary text-opacity-90 mb-2">
                  <span className="font-semibold text-lg">Next Steps</span>
                </p>
                <p className="text-primary text-opacity-80 text-lg">You will receive a confirmation email shortly with details about your purchase and access instructions.</p>
              </div>
              <div>
                <p className="text-primary text-opacity-90 mb-2">
                  <span className="font-semibold text-lg">Need Help?</span>
                </p>
                <p className="text-primary text-opacity-80 text-lg"><button onClick={() => navigateToTop('/contact')} className="text-tertiary-600 hover:text-tertiary-700 font-semibold bg-none border-none cursor-pointer p-0">Contact us</button> for any questions or concerns.</p>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* CTA Section */}
      <div className="bg-primary text-secondary py-10 md:py-16">
        <div className="container mx-auto px-4">
          <div className="max-w-2xl mx-auto text-center">
            <h2 className="text-2xl md:text-3xl font-bold mb-8 md:mb-10">What's Next?</h2>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <button
                onClick={() => navigateToTop('/programs')}
                className="w-full sm:w-48 md:w-56 inline-flex items-center justify-center px-4 sm:px-6 py-2 sm:py-2.5 border border-primary text-sm sm:text-base md:text-lg font-medium rounded-md text-secondary bg-tertiary-600 hover:bg-tertiary-700 transition-colors duration-200"
              >
                Explore Programs
              </button>
              <button
                onClick={() => navigateToTop('/')}
                className="w-full sm:w-48 md:w-56 inline-flex items-center justify-center px-4 sm:px-6 py-2 sm:py-2.5 border border-primary text-sm sm:text-base md:text-lg font-medium rounded-md text-secondary bg-tertiary-600 hover:bg-tertiary-700 transition-colors duration-200"
              >
                Return to Home
              </button>
            </div>
          </div>
        </div>
      </div>

    </div>
  );
};

export default PaymentSuccessPage;
