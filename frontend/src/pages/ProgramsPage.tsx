import React from 'react';
import { FiPlus, FiCheck, FiArrowRight } from 'react-icons/fi';
import { useCart } from '../context/CartContext';

const ProgramsPage: React.FC = () => {
  const { addItem, isInCart } = useCart();
  
  const programs = [
    {
      id: 2,
      title: '2 Week Program',
      description: 'Perfect for those looking to kickstart their fitness journey with a focused, short-term commitment.',
      image: 'https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b?ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=80'
    },
    {
      id: 4,
      title: '4 Week Program',
      description: 'A balanced program designed to build consistency and see noticeable progress in your fitness goals.',
      image: 'https://images.unsplash.com/photo-1571902943202-507ec2618e8f?ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=80'
    },
    {
      id: 6,
      title: '6 Week Program',
      description: 'Comprehensive training program for those committed to making lasting changes and seeing significant results.',
      image: 'https://images.unsplash.com/photo-1518611012118-696072aa579a?ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=80'
    }
  ];

  const handleAddToCart = (program: typeof programs[0]) => {
    addItem({
      title: program.title,
      duration: program.id,
      description: program.description,
      image: program.image
    });
  };

  return (
    <div className="w-full max-w-7xl mx-auto py-12 px-4 sm:px-6 lg:px-8">
      <div className="text-center mb-12">
        <h2 className="text-3xl font-bold text-gray-900 sm:text-4xl">Programs</h2>
        <p className="mt-4 text-xl text-gray-600">Tailored programs directed towards strength and hypertrophy.</p>
      </div>
      
      <div className="grid grid-cols-1 gap-8 sm:grid-cols-2 lg:grid-cols-3 w-full">
        {programs.map((program) => {
          const isAdded = isInCart(program.title);
          
          return (
            <div 
              key={program.id} 
              className="bg-white rounded-xl shadow-md overflow-hidden hover:shadow-xl transition-shadow duration-300 flex flex-col h-full"
            >
              {/* Image Section */}
              <div className="h-48 bg-gray-200 overflow-hidden">
                <img 
                  src={program.image} 
                  alt={program.title}
                  className="w-full h-full object-cover"
                />
              </div>

              {/* Content Section */}
              <div className="p-6 flex-1 flex flex-col">
                <div className="p-6 flex-grow">
                  <div className="flex justify-between items-start mb-2">
                    <h3 className="text-xl font-semibold text-gray-900">{program.title}</h3>
                    <span className="text-lg font-bold text-blue-600">${program.id === 2 ? '9.99' : program.id === 4 ? '19.99' : '29.99'}</span>
                  </div>
                  <p className="text-gray-600 mb-4">{program.description}</p>
                </div>
                
                <div className="mt-auto space-y-4">
                  <button 
                    onClick={() => handleAddToCart(program)}
                    disabled={isAdded}
                    className={`w-full flex items-center justify-center gap-2 ${
                      isAdded 
                        ? 'bg-green-100 text-green-700 cursor-not-allowed' 
                        : 'bg-blue-600 hover:bg-blue-700 text-white'
                    } font-medium py-3 px-6 rounded-lg transition-colors duration-200`}
                  >
                    {isAdded ? (
                      <>
                        <FiCheck className="text-lg" />
                        Added to Cart
                      </>
                    ) : (
                      <>
                        <FiPlus className="text-lg" />
                        Add to Cart
                      </>
                    )}
                  </button>
                  <button className="w-full flex items-center justify-center gap-2 text-blue-600 hover:text-blue-800 font-medium py-2 transition-colors duration-200">
                    Learn More
                    <FiArrowRight className="text-sm" />
                  </button>
                </div>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};

export default ProgramsPage;
