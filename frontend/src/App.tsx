import { useState, useEffect } from 'react';
import axios from 'axios';

interface HealthResponse {
  status: string;
  message: string;
}

function App() {
  const [health, setHealth] = useState<HealthResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchHealth = async () => {
      try {
        const response = await axios.get<HealthResponse>('/api/health');
        setHealth(response.data);
        setError(null);
      } catch (err) {
        setError('Failed to connect to the API. Make sure the backend server is running.');
      } finally {
        setLoading(false);
      }
    };

    fetchHealth();
  }, []);

  return (
    <div className="min-h-screen bg-gray-50">
      <header className="bg-white shadow">
        <div className="max-w-7xl mx-auto py-6 px-4 sm:px-6 lg:px-8">
          <h1 className="text-3xl font-bold text-gray-900">Brawny Originals</h1>
        </div>
      </header>
      <main>
        <div className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
          <div className="px-4 py-6 sm:px-0">
            <div className="border-2 border-dashed border-gray-200 rounded-lg p-8 text-center">
              {loading ? (
                <p className="text-gray-500">Checking API status...</p>
              ) : error ? (
                <div className="text-red-600">
                  <p>{error}</p>
                  <p className="mt-2 text-sm text-gray-600">
                    Make sure to start the backend server with: 
                    <code className="ml-1 px-2 py-1 bg-gray-100 rounded">
                      uvicorn main:app --reload
                    </code>
                  </p>
                </div>
              ) : (
                <div>
                  <p className="text-lg font-medium text-gray-900">
                    API Status: <span className="text-green-600">{health?.status}</span>
                  </p>
                  <p className="mt-1 text-gray-600">{health?.message}</p>
                </div>
              )}
            </div>
            <div className="mt-8">
              <h2 className="text-xl font-semibold text-gray-900 mb-4">Getting Started</h2>
              <div className="bg-white shadow overflow-hidden sm:rounded-lg">
                <div className="px-4 py-5 sm:p-6">
                  <p className="text-gray-700 mb-4">
                    Your full-stack application is ready to go! Here are the next steps:
                  </p>
                  <ul className="list-disc pl-5 space-y-2 text-gray-600">
                    <li>Start the backend server: <code className="bg-gray-100 px-2 py-1 rounded">cd backend &amp;&amp; uvicorn main:app --reload</code></li>
                    <li>Start the frontend: <code className="bg-gray-100 px-2 py-1 rounded">cd frontend &amp;&amp; npm install &amp;&amp; npm run dev</code></li>
                    <li>Visit <a href="http://localhost:5173" className="text-blue-600 hover:underline">http://localhost:5173</a></li>
                    <li>API documentation available at <a href="http://localhost:8000/docs" className="text-blue-600 hover:underline">http://localhost:8000/docs</a></li>
                  </ul>
                </div>
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}

export default App;
