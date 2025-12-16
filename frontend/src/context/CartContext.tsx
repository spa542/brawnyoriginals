import React, { createContext, useContext, useState, ReactNode } from 'react';

export type CartItem = {
  id: number;
  title: string;
  duration: number;
  description: string;
  image: string;
  price: number;
  priceId: string;
};

type CartContextType = {
  items: CartItem[];
  addItem: (item: Omit<CartItem, 'id' | 'price'> & { price?: number; priceId: string }) => void;
  removeItem: (id: number) => void;
  clearCart: () => void;
  isInCart: (title: string) => boolean;
};

const getPriceByDuration = (duration: number): number => {
  switch(duration) {
    case 2: return 9.99;
    case 4: return 19.99;
    case 6: return 29.99;
    default: return 0;
  }
};

const CartContext = createContext<CartContextType | undefined>(undefined);

export const CartProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const [items, setItems] = useState<CartItem[]>([]);

  const addItem = (item: Omit<CartItem, 'id' | 'price'> & { price?: number; priceId: string }) => {
    if (items.some(cartItem => cartItem.title === item.title)) {
      return; // Item already in cart
    }
    
    setItems(prevItems => [
      ...prevItems,
      {
        ...item,
        id: Date.now(), // Simple unique ID
        price: item.price ?? getPriceByDuration(item.duration),
        priceId: item.priceId
      },
    ]);
  };

  const removeItem = (id: number) => {
    setItems(prevItems => prevItems.filter(item => item.id !== id));
  };

  const clearCart = () => {
    setItems([]);
  };

  const isInCart = (title: string) => {
    return items.some(item => item.title === title);
  };

  return (
    <CartContext.Provider value={{ items, addItem, removeItem, clearCart, isInCart }}>
      {children}
    </CartContext.Provider>
  );
};

export const useCart = () => {
  const context = useContext(CartContext);
  if (context === undefined) {
    throw new Error('useCart must be used within a CartProvider');
  }
  return context;
};
