/**
 * Luxury Loading States
 * Full-screen loader with animated progress for AI generation
 */

import { motion, AnimatePresence } from 'framer-motion';
import { cn } from '../../utils/logger';

interface LoadingProps {
  size?: 'sm' | 'md' | 'lg';
  className?: string;
}

export const LoadingSpinner = ({ size = 'md', className }: LoadingProps) => {
  const sizes = {
    sm: 'w-5 h-5',
    md: 'w-8 h-8',
    lg: 'w-12 h-12',
  };

  return (
    <motion.div
      animate={{ rotate: 360 }}
      transition={{ duration: 1, repeat: Infinity, ease: 'linear' }}
      className={cn(
        'border-3 border-brand-gold/30 border-t-brand-gold rounded-full',
        sizes[size],
        className
      )}
    />
  );
};

interface GenerationLoaderProps {
  isOpen: boolean;
  progress: number;
  message: string;
  estimatedTime?: number;
}

export const GenerationLoader = ({
  isOpen,
  progress,
  message,
  estimatedTime,
}: GenerationLoaderProps) => {
  const messages = [
    'Analyzing your room...',
    'Generating design concepts...',
    'Applying furniture layout...',
    'Optimizing lighting...',
    'Adding final touches...',
  ];

  const currentMessage = message || messages[Math.floor((progress / 100) * messages.length)] || 'Designing your interior...';

  return (
    <AnimatePresence>
      {isOpen && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          className="fixed inset-0 z-50 flex items-center justify-center bg-brand-charcoal/95 backdrop-blur-sm"
        >
          <motion.div
            initial={{ scale: 0.9, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
            exit={{ scale: 0.9, opacity: 0 }}
            transition={{ duration: 0.3 }}
            className="text-center max-w-md w-full mx-4"
          >
            {/* Animated Rings */}
            <div className="relative w-32 h-32 mx-auto mb-8">
              <motion.div
                animate={{ rotate: 360 }}
                transition={{ duration: 3, repeat: Infinity, ease: 'linear' }}
                className="absolute inset-0 border-4 border-brand-gold/20 rounded-full"
              />
              <motion.div
                animate={{ rotate: -360 }}
                transition={{ duration: 2, repeat: Infinity, ease: 'linear' }}
                className="absolute inset-2 border-4 border-brand-gold/40 rounded-full"
              />
              <motion.div
                animate={{ rotate: 360 }}
                transition={{ duration: 1.5, repeat: Infinity, ease: 'linear' }}
                className="absolute inset-4 border-4 border-brand-gold/60 rounded-full"
              />
              <div className="absolute inset-0 flex items-center justify-center">
                <span className="text-3xl font-display font-bold text-brand-gold">
                  {Math.round(progress)}%
                </span>
              </div>
            </div>

            {/* Progress Bar */}
            <div className="w-full bg-white/10 rounded-full h-2 mb-6 overflow-hidden">
              <motion.div
                initial={{ width: 0 }}
                animate={{ width: `${progress}%` }}
                transition={{ duration: 0.5, ease: 'easeOut' }}
                className="h-full bg-gradient-to-r from-brand-gold to-brand-gold/80 rounded-full"
              />
            </div>

            {/* Status Message */}
            <motion.h3
              key={currentMessage}
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              className="text-2xl font-display font-semibold text-white mb-2"
            >
              {currentMessage}
            </motion.h3>

            {/* Estimated Time */}
            {estimatedTime && estimatedTime > 0 && (
              <p className="text-brand-gold/80 text-sm">
                Estimated time remaining: {estimatedTime}s
              </p>
            )}

            {/* Decorative Elements */}
            <div className="mt-8 flex justify-center gap-2">
              {[...Array(3)].map((_, i) => (
                <motion.div
                  key={i}
                  animate={{
                    scale: [1, 1.2, 1],
                    opacity: [0.5, 1, 0.5],
                  }}
                  transition={{
                    duration: 1.5,
                    repeat: Infinity,
                    delay: i * 0.2,
                  }}
                  className="w-2 h-2 bg-brand-gold rounded-full"
                />
              ))}
            </div>
          </motion.div>
        </motion.div>
      )}
    </AnimatePresence>
  );
};

interface SkeletonProps {
  className?: string;
  variant?: 'text' | 'rect' | 'circle';
  width?: string;
  height?: string;
}

export const Skeleton = ({
  className,
  variant = 'rect',
  width,
  height,
}: SkeletonProps) => {
  const variants = {
    text: 'rounded',
    rect: 'rounded-lg',
    circle: 'rounded-full',
  };

  return (
    <div
      className={cn(
        'bg-neutral-200 animate-shimmer bg-gradient-to-r from-neutral-200 via-neutral-300 to-neutral-200 bg-[length:200%_100%]',
        variants[variant],
        className
      )}
      style={{ width, height }}
    />
  );
};

export const CardSkeleton = () => (
  <div className="bg-white rounded-2xl shadow-soft p-6 space-y-4">
    <Skeleton variant="rect" height="200px" className="w-full" />
    <Skeleton variant="text" height="24px" className="w-3/4" />
    <Skeleton variant="text" height="16px" className="w-1/2" />
  </div>
);
