/**
 * Enterprise Sidebar Component
 * Luxury navigation with usage counter and smooth animations
 */

import { motion } from 'framer-motion';
import { Link, useLocation } from 'react-router-dom';
import { 
  HomeIcon, 
  PhotoIcon, 
  ArrowTrendingUpIcon,
  UserIcon,
  PlusIcon,
  SparklesIcon
} from '@heroicons/react/24/outline';
import { cn } from '../../utils/logger';
import { useGlobalStore, selectRemainingGenerations } from '../../store/globalStore';

interface NavItem {
  icon: React.ElementType;
  label: string;
  href: string;
  active?: boolean;
}

export const Sidebar = () => {
  const location = useLocation();
  const sidebarOpen = useGlobalStore((state) => state.sidebarOpen);
  const remainingGenerations = useGlobalStore(selectRemainingGenerations);

  const navItems: NavItem[] = [
    { icon: HomeIcon, label: 'Dashboard', href: '/dashboard' },
    { icon: PlusIcon, label: 'New Design', href: '/upload' },
    { icon: PhotoIcon, label: 'My Designs', href: '/history' },
    { icon: ArrowTrendingUpIcon, label: 'Compare', href: '/compare' },
    { icon: UserIcon, label: 'Profile', href: '/profile' },
  ];

  return (
    <motion.aside
      initial={{ x: -280 }}
      animate={{ x: sidebarOpen ? 0 : -280 }}
      transition={{ duration: 0.3, ease: [0.16, 1, 0.3, 1] }}
      className="fixed left-0 top-0 h-full w-72 bg-brand-charcoal text-white z-40 shadow-luxury"
    >
      {/* Logo Section */}
      <div className="p-8 mb-4">
        <Link to="/dashboard" className="flex items-center space-x-3">
          <motion.div 
            whileHover={{ scale: 1.05 }}
            className="w-12 h-12 bg-brand-gold rounded-xl flex items-center justify-center shadow-glow"
          >
            <SparklesIcon className="w-6 h-6 text-brand-charcoal" />
          </motion.div>
          <div>
            <h1 className="text-2xl font-display font-bold text-white">AntarAalay</h1>
            <p className="text-xs text-brand-gold/80 tracking-wider">AI INTERIOR DESIGN</p>
          </div>
        </Link>
      </div>

      {/* Navigation */}
      <nav className="px-4 space-y-1">
        {navItems.map((item, index) => {
          const isActive = location.pathname === item.href;
          
          return (
            <motion.div
              key={item.label}
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: index * 0.1, duration: 0.4 }}
            >
              <Link
                to={item.href}
                className={cn(
                  'flex items-center space-x-3 px-4 py-3 rounded-xl transition-all duration-300 group',
                  isActive 
                    ? 'bg-brand-gold text-brand-charcoal shadow-glow' 
                    : 'text-neutral-400 hover:text-white hover:bg-white/10'
                )}
              >
                <item.icon className={cn(
                  'w-5 h-5 transition-transform duration-300',
                  'group-hover:scale-110'
                )} />
                <span className="font-medium">{item.label}</span>
                
                {/* Active Indicator */}
                {isActive && (
                  <motion.div
                    layoutId="activeNav"
                    className="absolute right-4 w-2 h-2 bg-brand-charcoal rounded-full"
                  />
                )}
              </Link>
            </motion.div>
          );
        })}
      </nav>

      {/* Usage Counter Card */}
      <div className="absolute bottom-8 left-4 right-4">
        <motion.div
          whileHover={{ scale: 1.02 }}
          className="bg-gradient-to-br from-brand-gold/20 to-brand-gold/5 backdrop-blur-sm rounded-xl p-4 border border-brand-gold/30"
        >
          <div className="flex items-center justify-between mb-2">
            <span className="text-sm text-neutral-300">Daily Usage</span>
            <SparklesIcon className="w-4 h-4 text-brand-gold" />
          </div>
          
          <div className="flex items-end justify-between">
            <div>
              <span className="text-3xl font-display font-bold text-brand-gold">
                {remainingGenerations}
              </span>
              <span className="text-sm text-neutral-400 ml-1">/ 3 left</span>
            </div>
            
            {/* Progress Dots */}
            <div className="flex gap-1">
              {[...Array(3)].map((_, i) => (
                <div
                  key={i}
                  className={cn(
                    'w-2 h-2 rounded-full transition-colors duration-300',
                    i < remainingGenerations ? 'bg-brand-gold' : 'bg-white/20'
                  )}
                />
              ))}
            </div>
          </div>
          
          {remainingGenerations === 0 && (
            <p className="text-xs text-red-400 mt-2">
              Limit reached. Upgrade for more.
            </p>
          )}
        </motion.div>
      </div>
    </motion.aside>
  );
};
