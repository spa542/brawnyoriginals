import React, { useRef, useEffect, useState } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { FiShoppingCart, FiX, FiLoader } from 'react-icons/fi';
import { useCart } from '../context/CartContext';
import { getBaseUrl } from '../utils/helpers';
import { ReCAPTCHA } from './ReCAPTCHA';

const Navigation: React.FC = () => {
  const location = useLocation();
  const { items, removeItem, clearCart } = useCart();
  const [isCartOpen, setIsCartOpen] = useState(false);
  const [recaptchaToken, setRecaptchaToken] = useState('');
  const [isCheckingOut, setIsCheckingOut] = useState(false);
  const [error, setError] = useState<string | null>(null);
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

  const handleRecaptchaVerify = (token: string) => {
    setRecaptchaToken(token);
  };

  const handleCheckout = async () => {
    if (cartItems.length === 0) return;
    
    setIsCheckingOut(true);
    setError(null);
    
    try {
      if (!recaptchaToken) {
        throw new Error('reCAPTCHA verification is required');
      }

      const price_ids = cartItems.map(item => item.priceId);
      
      // Generate token with all items
      const baseUrl = getBaseUrl(); 
      const tokenResponse = await fetch(`${baseUrl}/api/payments/generate-token`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        credentials: 'same-origin',
        body: JSON.stringify({
          price_ids,
          captcha_token: recaptchaToken
        })
      });

      if (!tokenResponse.ok) {
        const errorData = await tokenResponse.json().catch(() => ({}));
        throw new Error(errorData.detail || 'Failed to generate token');
      }
      
      const { token: sessionToken } = await tokenResponse.json();
      
      // Create checkout session with all items
      const sessionResponse = await fetch(`${baseUrl}/api/payments/create-checkout-session`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        credentials: 'same-origin',
        body: JSON.stringify({
          token: sessionToken,
          price_ids: price_ids,
          quantity: 1, // Quantity per item - Always 1
          success_url: `${window.location.origin}/#/payment-success`,
          cancel_url: `${window.location.origin}/#/payment-cancel`
        })
      });

      if (!sessionResponse.ok) {
        const errorData = await sessionResponse.json().catch(() => ({}));
        throw new Error(errorData.detail || 'Failed to create checkout session');
      }
      
      const sessionData = await sessionResponse.json();
      
      // Redirect to Stripe Checkout
      window.location.href = sessionData.url;
      
    } catch (err) {
      console.error('Checkout error:', err);
      setError(err instanceof Error ? err.message : 'Failed to process checkout. Please try again.');
      setIsCheckingOut(false);
    }
  };

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
          <div className="hidden lg:block absolute left-1/2 transform -translate-x-1/2">
            <div className="flex space-x-8">
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
                          disabled={cartItems.length === 0}
                          className="flex-1 flex justify-center items-center px-4 py-2 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-primary bg-white hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
                        >
                          Clear Cart
                        </button>
                        <button 
                          type="button"
                          onClick={handleCheckout}
                          disabled={cartItems.length === 0 || isCheckingOut}
                          className={`flex-1 flex justify-center items-center px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white ${
                            cartItems.length === 0 
                              ? 'bg-gray-400 cursor-not-allowed' 
                              : isCheckingOut 
                                ? 'bg-tertiary-400' 
                                : 'bg-tertiary-600 hover:bg-tertiary-700'
                          }`}
                        >
                          {isCheckingOut ? (
                            <>
                              <FiLoader className="animate-spin -ml-1 mr-2 h-4 w-4" />
                              Processing...
                            </>
                          ) : cartItems.length === 0 ? (
                            'Cart is Empty'
                          ) : (
                            'Proceed to Checkout'
                          )}
                        </button>
                      </div>
                      {error && (
                        <div className="text-red-500 text-sm mt-2">
                          {error}
                        </div>
                      )}
                    </div>
                  </>
                )}
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Mobile menu - Show on screens smaller than lg (1024px) */}
      <div className="lg:hidden">
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
      
      {/* Hidden reCAPTCHA component */}
      <div style={{ display: 'none' }}>
        <ReCAPTCHA 
          sitekey="6Ldh-dorAAAAAG7kBeNcDUsLM5PtgfZPip2f9jwH"
          action="checkout"
          onVerify={handleRecaptchaVerify}
        />
      </div>
    </nav>
  );
};

export default Navigation;
