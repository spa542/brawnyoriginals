import React from 'react';
import { FiPlus, FiCheck } from 'react-icons/fi';

type ButtonVariant = 'default' | 'modal';

interface AddToCartButtonProps {
  isInCart: boolean;
  onClick: () => void;
  className?: string;
  disabled?: boolean;
  dataTestId?: string;
  variant?: ButtonVariant;
  comingSoon?: boolean;
}

const AddToCartButton: React.FC<AddToCartButtonProps> = ({
  isInCart,
  onClick,
  className = '',
  disabled = false,
  dataTestId = 'add-to-cart-button',
  variant = 'default',
  comingSoon = false
}) => {
  const baseStyles = 'flex items-center justify-center gap-2 font-medium transition-colors duration-200';
  
  const variantStyles = {
    default: `w-full border ${
      comingSoon 
        ? 'bg-yellow-100 text-yellow-800 border-primary cursor-not-allowed' 
        : isInCart
          ? 'bg-green-100 text-green-700 border-green-300 cursor-not-allowed' 
          : 'bg-tertiary-600 hover:bg-tertiary-700 text-white border-primary'
    } py-2 px-6 rounded-lg`,
    
    modal: `border ${
      comingSoon 
        ? 'bg-yellow-100 text-yellow-800 border-primary cursor-not-allowed' 
        : isInCart
          ? 'bg-green-100 text-green-700 border-green-300 cursor-not-allowed' 
          : 'bg-tertiary-600 hover:bg-tertiary-700 text-white border-primary'
    } py-2 px-6 rounded-lg`
  };

  return (
    <button
      onClick={onClick}
      disabled={comingSoon || isInCart || disabled}
      data-testid={dataTestId}
      className={`${baseStyles} ${variantStyles[variant]} ${className}`}
    >
      {comingSoon ? 'Coming Soon' : isInCart ? (
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
  );
};

export default AddToCartButton;
