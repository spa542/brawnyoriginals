import React, { useRef, useEffect, useState } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { FiShoppingCart, FiX } from 'react-icons/fi';
import { useCart } from '../context/CartContext';


const Navigation: React.FC = () => {
  const location = useLocation();
  const { items, removeItem, clearCart } = useCart();
  const [isCartOpen, setIsCartOpen] = useState(false);
  const cartRef = useRef<HTMLDivElement>(null);

  // Close cart when clicking outside
  useEffect(() => {
    function handleClickOutside(event: MouseEvent) {
      if (cartRef.current && !cartRef.current.contains(event.target as Node)) {
        setIsCartOpen(false);
      }
    }

    document.addEventListener('mousedown', handleClickOutside);
    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, []);

  const toggleCart = () => {
    setIsCartOpen(!isCartOpen);
  };

  const cartItems = items;
  const cartTotal = items.reduce((total, item) => total + (item.price || 0), 0);

  const navItems = [
    { path: '/', label: 'Home' },
    { path: '/programs', label: 'Programs' },
    { path: '/about', label: 'About' },
    { path: '/contact', label: 'Contact' },
  ];

  return (
    <nav className="bg-primary shadow-sm text-secondary">
      <div className="w-full px-8 lg:px-16">
        <div className="flex items-center justify-between h-24">
          {/* Left section - Logo */}
          <div className="flex-shrink-0">
            <Link to="/" className="flex items-center space-x-2">
              <div className="h-14 w-14 flex items-center justify-center">
                <img 
                  src={`${import.meta.env.PROD ? '/static/' : ''}images/brawny_originals_logo_white_no_bg.png`}
                  alt="Brawny Originals Logo"
                  className="h-full w-auto object-contain"
                />
              </div>
              <span className="text-2xl font-pacifico text-secondary hover:text-opacity-80 transition-colors duration-200">Brawny Originals</span>
            </Link>
          </div>
          
          {/* Center section - Navigation links */}
          <div className="absolute left-1/2 transform -translate-x-1/2">
            <div className="hidden sm:flex space-x-8">
              {navItems.map((item) => (
                <Link
                  key={item.path}
                  to={item.path}
                  className={`${
                    location.pathname === item.path
                      ? 'border-tertiary-500 text-secondary'
                      : 'border-transparent text-secondary text-opacity-80 hover:border-tertiary-400 hover:text-opacity-100'
                  } inline-flex items-center px-1 pt-1 border-b-2 text-base font-medium transition-colors duration-200`}
                >
                  {item.label}
                </Link>
              ))}
            </div>
          </div>
          
          {/* Right section - Shopping cart - pushed to the right */}
          <div className="ml-auto relative" ref={cartRef}>
            <button 
              onClick={toggleCart}
              className="relative p-2.5 rounded-full text-secondary text-opacity-80 hover:bg-opacity-20 hover:bg-secondary hover:text-opacity-100 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-tertiary-500 transition-colors duration-200"
              aria-label="Shopping cart"
            >
              <FiShoppingCart className="h-7 w-7" />
              {cartItems.length > 0 && (
                <span className="absolute top-0 right-0 inline-flex items-center justify-center px-2 py-1 text-xs font-bold leading-none text-secondary bg-tertiary-600 transform translate-x-1/2 -translate-y-1/2 rounded-full">
                  {cartItems.length}
                </span>
              )}
            </button>
            {isCartOpen && (
              <div className="absolute top-full right-0 w-80 mt-2 bg-white border border-gray-200 rounded-lg shadow-xl overflow-hidden z-50 transform transition-all duration-200 ease-in-out">
                <div className="p-4 border-b border-gray-200 bg-gray-50">
                  <h3 className="text-lg font-medium text-primary">Your Cart</h3>
                  <p className="text-sm text-gray-500">{cartItems.length} {cartItems.length === 1 ? 'item' : 'items'}</p>
                </div>
                
                {cartItems.length === 0 ? (
                  <div className="p-6 text-center text-gray-500">
                    <FiShoppingCart className="mx-auto h-12 w-12 text-gray-400" />
                    <p className="mt-2">Your cart is empty</p>
                  </div>
                ) : (
                  <>
                    <div className="max-h-96 overflow-y-auto">
                      <ul className="divide-y divide-gray-200">
                        {cartItems.map((item) => (
                          <li key={item.id} className="p-4 hover:bg-gray-50 transition-colors duration-150">
                            <div className="flex items-start w-full">
                              <div className="flex-shrink-0 h-12 w-12 rounded-md overflow-hidden bg-gray-100">
                                <img 
                                  src={item.image} 
                                  alt={item.title}
                                  className="h-full w-full object-cover"
                                />
                              </div>
                              <div className="ml-3 flex-1">
                                <div className="flex justify-between">
                                  <h4 className="text-sm font-medium text-primary">{item.title}</h4>
                                  <span className="text-sm font-medium text-primary">${item.price?.toFixed(2)}</span>
                                </div>
                                <p className="text-xs text-gray-500">{item.duration} weeks</p>
                              </div>
                              <button
                                onClick={(e) => {
                                  e.stopPropagation();
                                  removeItem(item.id);
                                }}
                                className="ml-4 text-gray-400 hover:text-tertiary-600"
                              >
                                <FiX size={16} />
                              </button>
                            </div>
                          </li>
                        ))}
                      </ul>
                    </div>
                    <div className="border-t border-gray-200 bg-gray-50 p-4 space-y-3">
                      <div className="flex justify-between text-base font-medium text-primary">
                        <p>Subtotal</p>
                        <p>${cartTotal.toFixed(2)}</p>
                      </div>
                      <div className="flex space-x-3">
                        <button 
                          onClick={() => clearCart()}
                          className="flex-1 flex justify-center items-center px-4 py-2 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-primary bg-white hover:bg-gray-50"
                        >
                          Clear Cart
                        </button>
                        <button 
                          className="flex-1 flex justify-center items-center px-4 py-2 border border-primary rounded-md shadow-sm text-sm font-medium text-white bg-tertiary-600 hover:bg-tertiary-700"
                        >
                          Checkout
                        </button>
                      </div>
                    </div>
                  </>
                )}
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Mobile menu */}
      <div className="sm:hidden">
        <div className="pt-2 pb-3 space-y-1">
          {navItems.map((item) => (
            <Link
              key={item.path}
              to={item.path}
              className={`${
                location.pathname === item.path
                  ? 'bg-tertiary-50 border-tertiary-500 text-tertiary-700'
                  : 'border-transparent text-secondary text-opacity-80 hover:bg-gray-50 hover:border-tertiary-300 hover:text-opacity-100'
              } block pl-3 pr-4 py-2 border-l-4 text-base font-medium transition-colors duration-200`}
            >
              {item.label}
            </Link>
          ))}
          <div className="px-3 py-2">
            <button 
              className="flex items-center text-secondary text-opacity-80 hover:text-opacity-100"
              aria-label="Shopping cart"
              onClick={toggleCart}
            >
              <FiShoppingCart className="h-5 w-5 mr-2" />
              Shopping Cart
            </button>
          </div>
        </div>
      </div>
    </nav>
  );
};

export default Navigation;
