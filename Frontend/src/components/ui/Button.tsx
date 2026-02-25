/**
 * Luxury Button Component
 * Enterprise-grade with animations and variants
 */

import { motion } from 'framer-motion';
import { cn } from '../../utils/logger';

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary' | 'outline' | 'ghost' | 'danger';
  size?: 'sm' | 'md' | 'lg' | 'xl';
  isLoading?: boolean;
  leftIcon?: React.ReactNode;
  rightIcon?: React.ReactNode;
  fullWidth?: boolean;
}

export const Button = ({
  children,
  variant = 'primary',
  size = 'md',
  isLoading = false,
  leftIcon,
  rightIcon,
  fullWidth = false,
  className,
  disabled,
  ...props
}: ButtonProps) => {
  const baseStyles = 'inline-flex items-center justify-center font-medium transition-all duration-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-offset-2';
  
  const variants = {
    primary: 'bg-brand-gold text-white hover:bg-brand-gold/90 hover:shadow-glow focus:ring-brand-gold',
    secondary: 'bg-brand-charcoal text-white hover:bg-brand-charcoal/90 hover:shadow-luxury focus:ring-brand-charcoal',
    outline: 'border-2 border-brand-gold text-brand-gold hover:bg-brand-gold/10 hover:shadow-soft focus:ring-brand-gold',
    ghost: 'text-brand-charcoal hover:bg-brand-beige hover:text-brand-charcoal focus:ring-brand-gold',
    danger: 'bg-red-500 text-white hover:bg-red-600 hover:shadow-soft focus:ring-red-500',
  };
  
  const sizes = {
    sm: 'px-4 py-2 text-sm',
    md: 'px-6 py-3 text-base',
    lg: 'px-8 py-4 text-lg',
    xl: 'px-12 py-6 text-xl',
  };
  
  return (
    <motion.button
      whileHover={{ scale: disabled || isLoading ? 1 : 1.02 }}
      whileTap={{ scale: disabled || isLoading ? 1 : 0.98 }}
      className={cn(
        baseStyles,
        variants[variant],
        sizes[size],
        fullWidth && 'w-full',
        (disabled || isLoading) && 'opacity-60 cursor-not-allowed',
        className
      )}
      disabled={disabled || isLoading}
    >
      {isLoading ? (
        <motion.div
          animate={{ rotate: 360 }}
          transition={{ duration: 1, repeat: Infinity, ease: 'linear' }}
          className="w-5 h-5 border-2 border-white border-t-transparent rounded-full mr-2"
        />
      ) : leftIcon ? (
        <span className="mr-2">{leftIcon}</span>
      ) : null}
      
      {children}
      
      {rightIcon && !isLoading && <span className="ml-2">{rightIcon}</span>}
    </motion.button>
  );
};
