import React from 'react';

const ProgramsPage: React.FC = () => {
  return (
    <div className="py-8">
      <h2 className="text-2xl font-bold mb-6">Our Programs</h2>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {[1, 2, 3].map((program) => (
          <div key={program} className="border rounded-lg p-6 shadow-sm hover:shadow-md transition-shadow">
            <h3 className="text-xl font-semibold mb-2">Program {program}</h3>
            <p className="text-gray-600 mb-4">
              Description of program {program} will go here. This is a sample description.
            </p>
            <button className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 transition-colors">
              Learn More
            </button>
          </div>
        ))}
      </div>
    </div>
  );
};

export default ProgramsPage;
