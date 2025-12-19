import React from 'react';
import { FiX } from 'react-icons/fi';
import AddToCartButton from './AddToCartButton';

interface Program {
  id: number;
  title: string;
  description: string;
  image: string;
  price: number;
  longDescription: string;
  duration: string;
  level: string;
  focus: string;
}

interface ProgramDetailsModalProps {
  isOpen: boolean;
  onClose: () => void;
  program: Program | null;
  isInCart: boolean;
  onAddToCart: (item: any) => void;
}

const ProgramDetailsModal: React.FC<ProgramDetailsModalProps> = ({ isOpen, onClose, program, isInCart, onAddToCart }) => {
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
                  <ul className="list-disc pl-6 text-secondary-700 space-y-1">
                    <li>Duration: {program.duration}</li>
                    <li>Level: {program.level}</li>
                    <li>Focus: {program.focus}</li>
                  </ul>
                </div>
                
                <div className="flex items-center justify-between pt-4 border-t border-secondary-200">
                  <span className="text-2xl font-bold text-tertiary-700">${program.price.toFixed(2)}</span>
                  <AddToCartButton 
                    isInCart={isInCart}
                    onClick={() => {
                      onAddToCart({
                        title: program.title,
                        duration: program.id,
                        description: program.description,
                        image: program.image,
                        price: program.price
                      });
                      onClose();
                    }}
                    dataTestId={`modal-add-to-cart-${program.id}`}
                    variant="modal"
                  />
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
