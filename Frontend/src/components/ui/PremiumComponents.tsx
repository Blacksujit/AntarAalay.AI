/**
 * Premium UI Components
 * AntarAalay.ai - Luxury Interior Design Components
 */

import { motion } from 'framer-motion';
import { cn } from '../../utils/cn';
import { designTokens } from '../../theme/designTokens';

// Glass Card Component
interface GlassCardProps {
  children: React.ReactNode;
  className?: string;
  variant?: 'light' | 'dark';
  hover?: boolean;
  onClick?: () => void;
}

export const GlassCard: React.FC<GlassCardProps> = ({ 
  children, 
  className, 
  variant = 'light',
  hover = true,
  onClick
}) => {
  return (
    <motion.div
      whileHover={hover ? { y: -2, scale: 1.02 } : {}}
      transition={{ duration: 0.3, ease: 'easeOut' }}
      onClick={onClick}
      className={cn(
        'backdrop-blur-xl rounded-2xl border p-6',
        variant === 'light' 
          ? 'bg-white/10 border-white/20 shadow-luxury'
          : 'bg-black/20 border-white/10 shadow-luxury',
        onClick && 'cursor-pointer',
        className
      )}
      style={{
        boxShadow: designTokens.shadows.luxury,
      }}
    >
      {children}
    </motion.div>
  );
};

// Premium Button Component
interface PremiumButtonProps {
  children: React.ReactNode;
  onClick?: () => void;
  variant?: 'primary' | 'secondary' | 'outline' | 'ghost';
  size?: 'sm' | 'md' | 'lg' | 'xl';
  loading?: boolean;
  disabled?: boolean;
  className?: string;
  leftIcon?: React.ReactNode;
  rightIcon?: React.ReactNode;
  fullWidth?: boolean;
}

export const PremiumButton: React.FC<PremiumButtonProps> = ({
  children,
  onClick,
  variant = 'primary',
  size = 'md',
  loading = false,
  disabled = false,
  className,
  leftIcon,
  rightIcon,
  fullWidth = false,
}) => {
  const baseClasses = 'inline-flex items-center justify-center font-medium rounded-xl transition-all duration-300 focus:outline-none focus:ring-2 focus:ring-offset-2';
  
  const variants = {
    primary: 'bg-gradient-to-r from-amber-500 to-amber-600 text-white shadow-luxury hover:shadow-glow focus:ring-amber-500',
    secondary: 'bg-white text-charcoal-900 shadow-soft hover:shadow-medium focus:ring-white',
    outline: 'border-2 border-amber-400 text-amber-600 bg-transparent hover:bg-amber-50 focus:ring-amber-400',
    ghost: 'text-charcoal-600 hover:bg-amber-50 focus:ring-amber-400',
  };
  
  const sizes = {
    sm: 'px-4 py-2 text-sm',
    md: 'px-6 py-3 text-base',
    lg: 'px-8 py-4 text-lg',
    xl: 'px-10 py-5 text-xl',
  };
  
  return (
    <motion.button
      whileTap={{ scale: 0.98 }}
      whileHover={{ scale: loading || disabled ? 1 : 1.05 }}
      transition={{ duration: 0.2 }}
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

// Design Preview Card
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
      <div className="relative overflow-hidden rounded-2xl shadow-luxury bg-white">
        {/* Image Container */}
        <div className="aspect-[4/3] overflow-hidden">
          <motion.img
            src={imageUrl}
            alt={title}
            className="w-full h-full object-cover"
            whileHover={{ scale: 1.1 }}
            transition={{ duration: 0.6, ease: 'easeOut' }}
          />
          
          {/* Overlay Gradient */}
          <div className="absolute inset-0 bg-gradient-to-t from-black/60 via-transparent to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300" />
          
          {/* Hover Actions */}
          <div className="absolute bottom-4 left-4 right-4 transform translate-y-full group-hover:translate-y-0 transition-transform duration-300">
            <div className="bg-white/95 backdrop-blur-sm rounded-xl p-3 shadow-luxury">
              <p className="text-sm font-medium text-charcoal-900 mb-1">View Design</p>
              <p className="text-xs text-charcoal-600">Click to explore details</p>
            </div>
          </div>
        </div>
        
        {/* Card Content */}
        <div className="p-5 bg-white">
          <h3 className="font-serif text-xl font-bold text-charcoal-900 mb-2">{title}</h3>
          <div className="flex items-center justify-between">
            <span className="text-sm text-amber-600 font-medium">{style}</span>
            {cost && (
              <span className="text-sm font-semibold text-charcoal-900">{cost}</span>
            )}
          </div>
        </div>
      </div>
    </motion.div>
  );
};

// Progress Ring Component
interface ProgressRingProps {
  progress: number;
  size?: number;
  strokeWidth?: number;
  className?: string;
}

export const ProgressRing: React.FC<ProgressRingProps> = ({
  progress,
  size = 120,
  strokeWidth = 8,
  className,
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
          stroke="#C6A75E"
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
        <span className="text-2xl font-bold text-charcoal-900">{progress}%</span>
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
          className="w-3 h-3 bg-amber-400 rounded-full"
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

export default {
  GlassCard,
  PremiumButton,
  DesignCard,
  ProgressRing,
  LoadingDots,
};
