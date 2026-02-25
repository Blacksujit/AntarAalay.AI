/**
 * Enterprise Top Navigation
 * Premium header with user avatar and quick actions
 */

import { motion } from 'framer-motion';
import { useNavigate } from 'react-router-dom';
import { 
  Bars3Icon, 
  BellIcon, 
  ArrowRightOnRectangleIcon 
} from '@heroicons/react/24/outline';
import { cn } from '../../utils/logger';
import { useGlobalStore, selectRemainingGenerations } from '../../store/globalStore';
import { useAuthStore } from '../../store/authStore';

export const TopNav = () => {
  const navigate = useNavigate();
  const toggleSidebar = useGlobalStore((state) => state.toggleSidebar);
  const remainingGenerations = useGlobalStore(selectRemainingGenerations);
  const { user, logout } = useAuthStore();

  const handleLogout = async () => {
    await logout();
    navigate('/login');
  };

  return (
    <motion.header
      initial={{ y: -80 }}
      animate={{ y: 0 }}
      transition={{ duration: 0.5, ease: [0.16, 1, 0.3, 1] }}
      className="fixed top-0 left-0 right-0 h-16 bg-white/90 backdrop-blur-lg border-b border-neutral-200 z-30"
    >
      <div className="h-full px-6 flex items-center justify-between max-w-[1920px] mx-auto">
        {/* Left Section */}
        <div className="flex items-center gap-4">
          <motion.button
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            onClick={toggleSidebar}
            className="p-2 rounded-lg hover:bg-neutral-100 transition-colors"
          >
            <Bars3Icon className="w-6 h-6 text-brand-charcoal" />
          </motion.button>

          {/* Breadcrumb / Page Title */}
          <div className="hidden md:flex items-center gap-2 text-sm text-neutral-500">
            <span>AntarAalay</span>
            <span className="text-neutral-300">/</span>
            <span className="text-brand-charcoal font-medium">Dashboard</span>
          </div>
        </div>

        {/* Center - Usage Indicator (Mobile) */}
        <div className="md:hidden flex items-center gap-2">
          <span className="text-sm text-neutral-600">
            {remainingGenerations} / 3
          </span>
          <div className="flex gap-1">
            {[...Array(3)].map((_, i) => (
              <div
                key={i}
                className={cn(
                  'w-2 h-2 rounded-full',
                  i < remainingGenerations ? 'bg-brand-gold' : 'bg-neutral-300'
                )}
              />
            ))}
          </div>
        </div>

        {/* Right Section */}
        <div className="flex items-center gap-4">
          {/* Notifications */}
          <motion.button
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            className="relative p-2 rounded-lg hover:bg-neutral-100 transition-colors"
          >
            <BellIcon className="w-5 h-5 text-brand-charcoal" />
            {/* Notification Badge */}
            <span className="absolute top-1 right-1 w-2 h-2 bg-red-500 rounded-full" />
          </motion.button>

          {/* User Profile */}
          <div className="flex items-center gap-3 pl-4 border-l border-neutral-200">
            <div className="hidden md:block text-right">
              <p className="text-sm font-medium text-brand-charcoal">
                {user?.displayName || 'Designer'}
              </p>
              <p className="text-xs text-neutral-500">
                {user?.email || 'user@antaraalay.ai'}
              </p>
            </div>

            <motion.div
              whileHover={{ scale: 1.05 }}
              className="relative"
            >
              {user?.photoURL ? (
                <img
                  src={user.photoURL}
                  alt="Profile"
                  className="w-10 h-10 rounded-full object-cover border-2 border-brand-gold/30"
                />
              ) : (
                <div className="w-10 h-10 rounded-full bg-brand-gold/20 flex items-center justify-center border-2 border-brand-gold/30">
                  <span className="text-brand-gold font-semibold">
                    {(user?.displayName || 'U')[0].toUpperCase()}
                  </span>
                </div>
              )}
              
              {/* Online Status */}
              <span className="absolute bottom-0 right-0 w-3 h-3 bg-green-500 rounded-full border-2 border-white" />
            </motion.div>

            {/* Logout Button */}
            <motion.button
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              onClick={handleLogout}
              className="hidden md:flex p-2 rounded-lg hover:bg-red-50 text-neutral-500 hover:text-red-600 transition-colors"
            >
              <ArrowRightOnRectangleIcon className="w-5 h-5" />
            </motion.button>
          </div>
        </div>
      </div>
    </motion.header>
  );
};
