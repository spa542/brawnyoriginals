import React from 'react';
import { FiX, FiPlus, FiCheck } from 'react-icons/fi';

interface ProgramDetailsModalProps {
  isOpen: boolean;
  onClose: () => void;
  program: {
    id: number;
    title: string;
    description: string;
    longDescription?: string;
    image: string;
    price: number;
  } | null;
  isInCart: boolean;
}

const ProgramDetailsModal: React.FC<ProgramDetailsModalProps> = ({ isOpen, onClose, program, isInCart }) => {
  if (!isOpen || !program) return null;

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div className="bg-white rounded-xl max-w-4xl w-full max-h-[90vh] overflow-y-auto">
        <div className="sticky top-0 bg-white p-4 border-b border-secondary-200 flex justify-between items-center">
          <h2 className="text-2xl font-bold text-primary-900">{program.title}</h2>
          <button 
            onClick={onClose}
            className="text-secondary-600 hover:text-primary-700 focus:outline-none"
            aria-label="Close modal"
          >
            <FiX className="h-6 w-6" />
          </button>
        </div>
        
        <div className="p-6">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
            <div className="h-64 md:h-full rounded-lg overflow-hidden">
              <img 
                src={program.image} 
                alt={program.title}
                className="w-full h-full object-cover"
              />
            </div>
            
            <div>
              <div className="mb-6">
                <h3 className="text-xl font-semibold text-primary-900 mb-2">Program Overview</h3>
                <p className="text-secondary-800">
                  {program.longDescription || 'Detailed program description will be added here. This will include comprehensive information about the training methodology, what to expect, and the benefits of this program.'}
                </p>
              </div>
              
              <div className="space-y-4">
                <div className="p-4 bg-secondary-50 rounded-lg">
                  <h4 className="font-medium text-primary-900 mb-2">Program Details</h4>
                  <ul className="space-y-2 text-secondary-800">
                    <li>• Duration: {program.id} weeks</li>
                    <li>• Level: All levels</li>
                    <li>• Focus: Strength & Hypertrophy</li>
                    <li>• Equipment: Gym or Home Equipment</li>
                  </ul>
                </div>
                
                <div className="flex items-center justify-between pt-4 border-t border-secondary-200">
                  <span className="text-2xl font-bold text-tertiary-700">${program.price.toFixed(2)}</span>
                  {isInCart ? (
                    <button 
                      className="bg-secondary-200 text-primary-800 font-medium py-2 px-6 rounded-lg cursor-not-allowed flex items-center gap-2"
                      disabled
                    >
                      <FiCheck className="text-lg" />
                      Added to Cart
                    </button>
                  ) : (
                    <button 
                      className="bg-tertiary-600 hover:bg-tertiary-700 text-white font-medium py-2 px-6 rounded-lg border border-primary transition-colors duration-200 flex items-center gap-2"
                      onClick={() => {
                        onClose();
                        const addToCartButton = document.querySelector(`[data-program-title="${program.title}"]`);
                        if (addToCartButton) {
                          (addToCartButton as HTMLElement).click();
                        }
                      }}
                    >
                      <FiPlus className="text-lg" />
                      Add to Cart
                    </button>
                  )}
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ProgramDetailsModal;
