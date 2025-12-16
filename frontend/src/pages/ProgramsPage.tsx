import React, { useState } from 'react';
import { FiArrowRight } from 'react-icons/fi';
import AddToCartButton from '../components/AddToCartButton';
import { useCart } from '../context/CartContext';
import ProgramDetailsModal from '../components/ProgramDetailsModal';

interface Program {
  id: number;
  title: string;
  description: string;
  image: string;
  price: number;
  priceId: string;  // Stripe Price ID
  longDescription: string;
  duration: string;
  level: string;
  focus: string;
}

const ProgramsPage: React.FC = () => {
  const { addItem, isInCart } = useCart();
  const [selectedProgram, setSelectedProgram] = useState<Program | null>(null);
  const [isModalOpen, setIsModalOpen] = useState(false);
  
  const programs: Program[] = [
    {
      id: 4,
      title: 'Program Blue (4 Week Program)',
      description: 'A short and simple program designed for gaining muscular hypertrophy.',
      image: `${import.meta.env.PROD ? '/static/' : ''}images/4_week_hypertrophy_program_high_res.jpeg`,
      price: 19.99,
      priceId: import.meta.env.PROD 
        ? 'price_1Sf0Jj2cxMNEOVDK1vgR9A6A'  // Production price ID
        : 'price_1ScWdxK5tsm2JTU1Zogy9QKZ', // Development/Test price ID
      longDescription: 'This program is designed for gaining muscular hypertrophy. This program is great for beginners and intermediates, and provides a variety of exercise selection to choose from. It is very straightforward and simple to follow.',
      duration: '4 weeks',
      level: 'Beginner to Intermediate',
      focus: 'Hypertrophy'
    },
    {
      id: 6,
      title: 'Project Genesis (17 Week Prep Program)',
      description: 'My full workout regimen, nutrition guide and preparation for my first bodybuilding competition.',
      image: `${import.meta.env.PROD ? '/static/' : ''}images/program_genesis_high_res_2.jpeg`,
      price: 59.99,
      priceId: import.meta.env.PROD
        ? 'price_1Sf0Js2cxMNEOVDKqVYTmhvZ'  // Production price ID
        : 'price_1ScWd9K5tsm2JTU1tjTXlwc8', // Development/Test price ID
      longDescription: 'This program is designed for maintenance of muscle and strength while cutting weight. This program is exactly what I followed for my first bodybuilding show. It is catered toward anyone who is intermediate or advanced getting ready for a show. The information provided in this program is very in depth, but still straightforward to follow.',
      duration: '17 weeks',
      level: 'Intermediate to Advanced',
      focus: 'Muscle Maintenance and Strength'
    }
  ];

  const handleAddToCart = (program: Program) => {
    addItem({
      title: program.title,
      duration: program.id,
      description: program.description,
      image: program.image,
      price: program.price,
      priceId: program.priceId
    });
  };

  const openProgramDetails = (program: Program) => {
    setSelectedProgram(program);
    setIsModalOpen(true);
  };

  const closeProgramDetails = () => {
    setIsModalOpen(false);
  };

  const renderProgramCard = (program: Program) => (
    <div 
      className="bg-white rounded-xl shadow-md overflow-hidden hover:shadow-xl transition-shadow duration-300 flex flex-col h-full w-full"
    >
      {/* Image Section */}
      <div className="h-64 bg-gray-200 overflow-hidden">
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
          <AddToCartButton 
            isInCart={isInCart(program.title)}
            onClick={() => handleAddToCart(program)}
            dataTestId={`add-to-cart-${program.id}`}
            className="py-3"
          />
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
  );

  return (
    <div className="w-full max-w-7xl mx-auto py-12 px-4 sm:px-6 lg:px-8">
      <div className="text-center mb-12">
        <h2 className="text-3xl font-bold text-gray-900 sm:text-4xl">Programs</h2>
        <p className="mt-4 text-xl text-gray-600">Tailored programs directed towards strength and hypertrophy.</p>
      </div>
      
      <div className="w-full space-y-8">
        {programs.length === 1 ? (
          <div className="flex justify-center">
            <div className="w-full max-w-md">
              {renderProgramCard(programs[0])}
            </div>
          </div>
        ) : programs.length === 2 ? (
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-8 max-w-4xl mx-auto">
            {programs.map(program => (
              <div key={program.id} className="w-full">
                {renderProgramCard(program)}
              </div>
            ))}
          </div>
        ) : (
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-8 max-w-6xl mx-auto">
            {programs.map(program => (
              <div key={program.id} className="w-full">
                {renderProgramCard(program)}
              </div>
            ))}
          </div>
        )}
      </div>
      
      {/* Program Details Modal */}
      <ProgramDetailsModal
        isOpen={isModalOpen}
        onClose={closeProgramDetails}
        program={selectedProgram}
        isInCart={selectedProgram ? isInCart(selectedProgram.title) : false}
        onAddToCart={handleAddToCart}
      />
    </div>
  );
};

export default ProgramsPage;
