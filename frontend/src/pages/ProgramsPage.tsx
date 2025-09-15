import React, { useState } from 'react';
import { FiPlus, FiCheck, FiArrowRight } from 'react-icons/fi';
import { useCart } from '../context/CartContext';
import ProgramDetailsModal from '../components/ProgramDetailsModal';

interface Program {
  id: number;
  title: string;
  description: string;
  image: string;
  price: number;
  longDescription?: string;
}

const ProgramsPage: React.FC = () => {
  const { addItem, isInCart } = useCart();
  const [selectedProgram, setSelectedProgram] = useState<Program | null>(null);
  const [isModalOpen, setIsModalOpen] = useState(false);
  
  const programs: Program[] = [
    {
      id: 2,
      title: '2 Week Program',
      description: 'Perfect for those looking to kickstart their fitness journey with a focused, short-term commitment.',
      image: 'https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b?ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=80',
      price: 9.99,
      longDescription: 'This 2-week program is designed to give you a solid foundation in strength training. You\'ll learn proper form, build fundamental movement patterns, and establish a consistent workout routine. Perfect for beginners or those returning to fitness after a break.'
    },
    {
      id: 4,
      title: '4 Week Program',
      description: 'A balanced program designed to build consistency and see noticeable progress in your fitness goals.',
      image: 'https://images.unsplash.com/photo-1571902943202-507ec2618e8f?ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=80',
      price: 19.99,
      longDescription: 'Our 4-week program takes your fitness to the next level with progressive overload and varied training techniques. You\'ll see noticeable improvements in strength, endurance, and body composition. Includes detailed workout plans and nutrition guidance.'
    },
    {
      id: 6,
      title: '6 Week Program',
      description: 'Comprehensive training program for those committed to making lasting changes and seeing significant results.',
      image: 'https://images.unsplash.com/photo-1518611012118-696072aa579a?ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=80',
      price: 29.99,
      longDescription: 'This comprehensive 6-week program is designed for maximum results. Combining strength training, conditioning, and recovery protocols, you\'ll experience significant improvements in performance and physique. Includes personalized support and progress tracking.'
    }
  ];

  const handleAddToCart = (program: Program) => {
    addItem({
      title: program.title,
      duration: program.id,
      description: program.description,
      image: program.image,
      price: program.price
    });
  };

  const openProgramDetails = (program: Program) => {
    setSelectedProgram(program);
    setIsModalOpen(true);
  };

  const closeProgramDetails = () => {
    setIsModalOpen(false);
  };

  return (
    <div className="w-full max-w-7xl mx-auto py-12 px-4 sm:px-6 lg:px-8">
      <div className="text-center mb-12">
        <h2 className="text-3xl font-bold text-gray-900 sm:text-4xl">Programs</h2>
        <p className="mt-4 text-xl text-gray-600">Tailored programs directed towards strength and hypertrophy.</p>
      </div>
      
      <div className="grid grid-cols-1 gap-8 sm:grid-cols-2 lg:grid-cols-3 w-full">
        {programs.map((program) => (
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
              <div className="flex-grow">
                <div className="flex justify-between items-start mb-2">
                  <h3 className="text-xl font-semibold text-gray-900">{program.title}</h3>
                  <span className="text-lg font-bold text-tertiary-600">${program.price}</span>
                </div>
                <p className="text-gray-600 mb-4">{program.description}</p>
              </div>
              
              <div className="mt-auto space-y-4">
                <button 
                  onClick={() => handleAddToCart(program)}
                  disabled={isInCart(program.title)}
                  data-program-title={program.title}
                  className={`w-full flex items-center justify-center gap-2 ${
                    isInCart(program.title)
                      ? 'bg-green-100 text-green-700 cursor-not-allowed' 
                      : 'bg-tertiary-600 hover:bg-tertiary-700 text-white'
                  } font-medium py-3 px-6 rounded-lg transition-colors duration-200`}
                >
                  {isInCart(program.title) ? (
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
                <button 
                  onClick={() => openProgramDetails(program)}
                  className="w-full text-center text-tertiary-600 hover:text-tertiary-800 font-medium py-2 px-4 rounded-lg transition-colors duration-200"
                >
                  Learn More
                  <FiArrowRight className="inline-block ml-1" />
                </button>
              </div>
            </div>
          </div>
        ))}
      </div>
      
      {/* Program Details Modal */}
      <ProgramDetailsModal
        isOpen={isModalOpen}
        onClose={closeProgramDetails}
        program={selectedProgram}
        isInCart={selectedProgram ? isInCart(selectedProgram.title) : false}
      />
    </div>
  );
};

export default ProgramsPage;
