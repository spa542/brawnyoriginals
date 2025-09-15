import { HashRouter as Router, Routes, Route } from 'react-router-dom';
import { CartProvider } from './context/CartContext';
import Navigation from './components/Navigation';
import BottomNavigation from './components/BottomNavigation';
import HomePage from './pages/HomePage';
import AboutPage from './pages/AboutPage';
import ProgramsPage from './pages/ProgramsPage';
import ContactPage from './pages/ContactPage';

function App() {
  return (
    <CartProvider>
      <Router>
        <div className="min-h-screen flex flex-col">
          <Navigation />
          <main className="flex-grow w-full">
            <Routes>
              <Route path="/" element={<HomePage />} />
              <Route path="/about" element={<AboutPage />} />
              <Route path="/programs" element={
                <div className="w-full">
                  <ProgramsPage />
                </div>
              } />
              <Route path="/contact" element={
                <div className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
                  <ContactPage />
                </div>
              } />
            </Routes>
          </main>
          <BottomNavigation />
        </div>
      </Router>
    </CartProvider>
  );
}

export default App;
