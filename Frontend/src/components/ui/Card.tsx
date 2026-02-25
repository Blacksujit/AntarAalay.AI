/**
 * Luxury Card Component
 * Enterprise-grade with hover effects and glassmorphism
 */

import { motion } from 'framer-motion';
import { cn } from '../../utils/logger';

interface CardProps {
  children: React.ReactNode;
  className?: string;
  variant?: 'default' | 'glass' | 'elevated';
  hover?: boolean;
  onClick?: () => void;
}

export const Card = ({
  children,
  className,
  variant = 'default',
  hover = true,
  onClick,
}: CardProps) => {
  const variants = {
    default: 'bg-white shadow-soft',
    glass: 'bg-white/80 backdrop-blur-lg shadow-glass border border-white/20',
    elevated: 'bg-white shadow-luxury',
  };

  return (
    <motion.div
      whileHover={hover ? { 
        y: -4, 
        boxShadow: '0 20px 40px rgba(0, 0, 0, 0.15)',
        transition: { duration: 0.3 }
      } : undefined}
      className={cn(
        'rounded-2xl overflow-hidden transition-all duration-300',
        variants[variant],
        onClick && 'cursor-pointer',
        className
      )}
      onClick={onClick}
    >
      {children}
    </motion.div>
  );
};

interface CardHeaderProps {
  children: React.ReactNode;
  className?: string;
}

export const CardHeader = ({ children, className }: CardHeaderProps) => (
  <div className={cn('px-6 py-4 border-b border-neutral-200', className)}>
    {children}
  </div>
);

interface CardContentProps {
  children: React.ReactNode;
  className?: string;
}

export const CardContent = ({ children, className }: CardContentProps) => (
  <div className={cn('p-6', className)}>
    {children}
  </div>
);

interface CardFooterProps {
  children: React.ReactNode;
  className?: string;
}

export const CardFooter = ({ children, className }: CardFooterProps) => (
  <div className={cn('px-6 py-4 border-t border-neutral-200 bg-neutral-50', className)}>
    {children}
  </div>
);
