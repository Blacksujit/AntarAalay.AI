/**
 * Premium UI Components
 * AntarAalay.ai - Luxury Interior Design Components
 */

import { motion } from 'framer-motion';
import { cn } from '../../utils/cn';

// Premium Button Component
interface ButtonProps {
  children: React.ReactNode;
  variant?: 'primary' | 'secondary' | 'outline' | 'ghost';
  size?: 'sm' | 'md' | 'lg' | 'xl';
  loading?: boolean;
  disabled?: boolean;
  className?: string;
  leftIcon?: React.ReactNode;
  rightIcon?: React.ReactNode;
  fullWidth?: boolean;
  onClick?: () => void;
}

export const Button: React.FC<ButtonProps> = ({
  children,
  variant = 'primary',
  size = 'md',
  loading = false,
  disabled = false,
  className,
  leftIcon,
  rightIcon,
  fullWidth = false,
  onClick,
}) => {
  const baseClasses = 'inline-flex items-center justify-center font-medium rounded-2xl transition-all duration-300 focus:outline-none focus:ring-2 focus:ring-offset-2';
  
  const variants = {
    primary: 'bg-gradient-to-r from-gold to-amber-600 text-white shadow-large hover:shadow-glow focus:ring-gold',
    secondary: 'bg-white text-charcoal shadow-medium hover:shadow-large focus:ring-white',
    outline: 'border-2 border-gold text-gold bg-transparent hover:bg-gold hover:text-white focus:ring-gold',
    ghost: 'text-charcoal hover:bg-stone focus:ring-stone',
  };
  
  const sizes = {
    sm: 'h-10 px-4 text-sm',
    md: 'h-12 px-6 text-base',
    lg: 'h-14 px-8 text-lg',
    xl: 'h-16 px-10 text-xl',
  };
  
  return (
    <motion.button
      whileTap={{ scale: 0.98 }}
      whileHover={{ scale: loading || disabled ? 1 : 1.02 }}
      transition={{ duration: 0.2, ease: 'easeOut' }}
      onClick={onClick}
      disabled={loading || disabled}
      className={cn(
        baseClasses,
        variants[variant],
        sizes[size],
        fullWidth && 'w-full',
        (loading || disabled) && 'opacity-50 cursor-not-allowed',
        className
      )}
    >
      {loading && (
        <motion.div
          animate={{ rotate: 360 }}
          transition={{ duration: 1, repeat: Infinity, ease: 'linear' }}
          className="w-4 h-4 border-2 border-current border-t-transparent rounded-full mr-2"
        />
      )}
      {!loading && leftIcon && <span className="mr-2">{leftIcon}</span>}
      {children}
      {!loading && rightIcon && <span className="ml-2">{rightIcon}</span>}
    </motion.button>
  );
};

// Glass Card Component
interface CardProps {
  children: React.ReactNode;
  className?: string;
  variant?: 'default' | 'glass' | 'elevated';
  hover?: boolean;
  onClick?: () => void;
}

export const Card: React.FC<CardProps> = ({ 
  children, 
  className, 
  variant = 'default',
  hover = true,
  onClick
}) => {
  const variants = {
    default: 'bg-white shadow-medium',
    glass: 'bg-glass backdrop-blur-xl border border-white/20 shadow-large',
    elevated: 'bg-white shadow-large',
  };
  
  return (
    <motion.div
      whileHover={hover && !onClick ? { y: -4, scale: 1.01 } : {}}
      transition={{ duration: 0.3, ease: 'easeOut' }}
      onClick={onClick}
      className={cn(
        'rounded-3xl p-6 transition-all duration-300',
        variants[variant],
        onClick && 'cursor-pointer hover:shadow-xl',
        className
      )}
    >
      {children}
    </motion.div>
  );
};

// Progress Ring Component
interface ProgressRingProps {
  progress: number;
  size?: number;
  strokeWidth?: number;
  className?: string;
  color?: string;
}

export const ProgressRing: React.FC<ProgressRingProps> = ({
  progress,
  size = 120,
  strokeWidth = 8,
  className,
  color = '#BFA46F'
}) => {
  const radius = (size - strokeWidth) / 2;
  const circumference = radius * 2 * Math.PI;
  const strokeDashoffset = circumference - (progress / 100) * circumference;
  
  return (
    <div className={cn('relative inline-flex items-center justify-center', className)}>
      <svg
        width={size}
        height={size}
        className="transform -rotate-90"
      >
        {/* Background circle */}
        <circle
          cx={size / 2}
          cy={size / 2}
          r={radius}
          stroke="#E5E7EB"
          strokeWidth={strokeWidth}
          fill="none"
        />
        {/* Progress circle */}
        <motion.circle
          cx={size / 2}
          cy={size / 2}
          r={radius}
          stroke={color}
          strokeWidth={strokeWidth}
          fill="none"
          strokeDasharray={circumference}
          strokeDashoffset={strokeDashoffset}
          strokeLinecap="round"
          initial={{ strokeDashoffset: circumference }}
          animate={{ strokeDashoffset }}
          transition={{ duration: 0.5, ease: 'easeOut' }}
        />
      </svg>
      <div className="absolute inset-0 flex items-center justify-center">
        <span className="text-2xl font-bold text-charcoal">{progress}%</span>
      </div>
    </div>
  );
};

// Loading Dots Component
export const LoadingDots: React.FC<{ className?: string }> = ({ className }) => {
  return (
    <div className={cn('flex space-x-2', className)}>
      {[0, 1, 2].map((index) => (
        <motion.div
          key={index}
          className="w-3 h-3 bg-gold rounded-full"
          animate={{
            scale: [1, 1.5, 1],
            opacity: [1, 0.5, 1],
          }}
          transition={{
            duration: 1.5,
            repeat: Infinity,
            delay: index * 0.2,
            ease: 'easeInOut',
          }}
        />
      ))}
    </div>
  );
};

// Shimmer Loader Component
interface ShimmerProps {
  className?: string;
  height?: string;
}

export const Shimmer: React.FC<ShimmerProps> = ({ className, height = 'h-4' }) => {
  return (
    <div className={cn('relative overflow-hidden bg-gray-200 rounded', height, className)}>
      <motion.div
        className="absolute inset-0 bg-gradient-to-r from-transparent via-white to-transparent opacity-30"
        animate={{ x: ['-100%', '100%'] }}
        transition={{ duration: 1.5, repeat: Infinity, ease: 'linear' }}
      />
    </div>
  );
};

// Design Card Component
interface DesignCardProps {
  title: string;
  imageUrl: string;
  style: string;
  cost?: string;
  onClick?: () => void;
  className?: string;
}

export const DesignCard: React.FC<DesignCardProps> = ({
  title,
  imageUrl,
  style,
  cost,
  onClick,
  className,
}) => {
  return (
    <motion.div
      whileHover={{ y: -8, scale: 1.02 }}
      transition={{ duration: 0.3, ease: 'easeOut' }}
      onClick={onClick}
      className={cn('group cursor-pointer', className)}
    >
      <Card variant="elevated" className="overflow-hidden p-0">
        {/* Image Container */}
        <div className="aspect-[4/3] overflow-hidden relative">
          <motion.img
            src={imageUrl}
            alt={title}
            className="w-full h-full object-cover"
            whileHover={{ scale: 1.1 }}
            transition={{ duration: 0.6, ease: 'easeOut' }}
          />
          
          {/* Overlay Gradient */}
          <div className="absolute inset-0 bg-gradient-to-t from-charcoal/60 via-transparent to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300" />
          
          {/* Hover Actions */}
          <div className="absolute bottom-4 left-4 right-4 transform translate-y-full group-hover:translate-y-0 transition-transform duration-300">
            <div className="bg-white/95 backdrop-blur-sm rounded-2xl p-4 shadow-large">
              <p className="text-sm font-medium text-charcoal mb-1">View Design</p>
              <p className="text-xs text-text-secondary">Click to explore details</p>
            </div>
          </div>
        </div>
        
        {/* Card Content */}
        <div className="p-6">
          <h3 className="font-serif text-xl font-bold text-charcoal mb-2">{title}</h3>
          <div className="flex items-center justify-between">
            <span className="text-sm font-medium text-gold">{style}</span>
            {cost && (
              <span className="text-sm font-semibold text-charcoal">{cost}</span>
            )}
          </div>
        </div>
      </Card>
    </motion.div>
  );
};

export default {
  Button,
  Card,
  ProgressRing,
  LoadingDots,
  Shimmer,
  DesignCard,
};
