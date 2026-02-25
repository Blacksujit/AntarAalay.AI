/**
 * Premium Dashboard
 * AntarAalay.ai - Luxury Interior Design Studio Dashboard
 */

import { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { useNavigate } from 'react-router-dom';
import { 
  PlusIcon,
  PhotoIcon,
  ArrowTrendingUpIcon,
  SparklesIcon,
  HomeIcon,
  UserIcon,
  ClockIcon,
  EyeIcon,
  HeartIcon,
  Cog6ToothIcon,
  ArrowRightIcon
} from '@heroicons/react/24/outline';
import { useQuery } from '@tanstack/react-query';
import { useAuthStore } from '../../store/authStore';
import { Button, Card, DesignCard } from '../../components/ui';

// Mock data
const mockDesigns = [
  {
    id: '1',
    title: 'Modern Living Sanctuary',
    imageUrl: 'https://images.unsplash.com/photo-1586023492125-27b2c045efd7?w=600&h=400&fit=crop',
    style: 'Contemporary',
    cost: '$45,000',
    createdAt: '2024-01-15',
    status: 'completed',
  },
  {
    id: '2',
    title: 'Minimalist Bedroom Retreat',
    imageUrl: 'https://images.unsplash.com/photo-1560185007-c5ca9d2c014d?w=600&h=400&fit=crop',
    style: 'Minimalist',
    cost: '$32,000',
    createdAt: '2024-01-14',
    status: 'completed',
  },
  {
    id: '3',
    title: 'Luxury Kitchen Transformation',
    imageUrl: 'https://images.unsplash.com/photo-1556909114-f6e7ad7d3136?w=600&h=400&fit=crop',
    style: 'High-End Modern',
    cost: '$65,000',
    createdAt: '2024-01-13',
    status: 'in-progress',
  },
];

const mockStats = {
  totalDesigns: 12,
  thisMonth: 3,
  avgCost: 42000,
  completionRate: 85,
  favoriteStyle: 'Contemporary',
};

export const PremiumDashboard: React.FC = () => {
  const navigate = useNavigate();
  const { user } = useAuthStore();
  const [greeting, setGreeting] = useState('');
  
  // Set greeting based on time
  useEffect(() => {
    const hour = new Date().getHours();
    if (hour < 12) setGreeting('Good morning');
    else if (hour < 17) setGreeting('Good afternoon');
    else setGreeting('Good evening');
  }, []);
  
  // Mock API calls
  const { data: designs, isLoading } = useQuery({
    queryKey: ['userDesigns'],
    queryFn: () => Promise.resolve(mockDesigns),
    staleTime: 5 * 60 * 1000,
  });
  
  // Navigation items
  const navItems = [
    { icon: HomeIcon, label: 'Dashboard', active: true },
    { icon: PhotoIcon, label: 'Designs', active: false },
    { icon: PlusIcon, label: 'Create', active: false },
    { icon: ClockIcon, label: 'History', active: false },
    { icon: UserIcon, label: 'Profile', active: false },
  ];
  
  if (!user) {
    navigate('/login');
    return null;
  }
  
  return (
    <div className="min-h-screen bg-stone">
      {/* Left Navigation */}
      <motion.div
        initial={{ x: -100 }}
        animate={{ x: 0 }}
        transition={{ duration: 0.6, ease: 'easeOut' }}
        className="fixed left-0 top-0 h-full w-20 bg-white shadow-large z-40"
      >
        <div className="flex flex-col items-center py-8 space-y-8">
          {/* Logo */}
          <motion.div
            whileHover={{ scale: 1.1 }}
            className="w-12 h-12 bg-gradient-to-br from-gold to-amber-600 rounded-2xl flex items-center justify-center shadow-glow"
          >
            <HomeIcon className="w-6 h-6 text-white" />
          </motion.div>
          
          {/* Navigation Items */}
          <nav className="flex flex-col space-y-6">
            {navItems.map((item, index) => (
              <motion.button
                key={item.label}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.1 + index * 0.1 }}
                whileHover={{ scale: 1.1 }}
                whileTap={{ scale: 0.95 }}
                className={`w-12 h-12 rounded-2xl flex items-center justify-center transition-all duration-300 ${
                  item.active
                    ? 'bg-gold text-white shadow-glow'
                    : 'text-text-secondary hover:bg-stone hover:text-charcoal'
                }`}
              >
                <item.icon className="w-5 h-5" />
              </motion.button>
            ))}
          </nav>
          
          {/* Settings */}
          <motion.button
            whileHover={{ scale: 1.1 }}
            whileTap={{ scale: 0.95 }}
            className="w-12 h-12 rounded-2xl flex items-center justify-center text-text-secondary hover:bg-stone hover:text-charcoal transition-all duration-300 mt-auto"
          >
            <Cog6ToothIcon className="w-5 h-5" />
          </motion.button>
        </div>
      </motion.div>
      
      {/* Main Content */}
      <div className="ml-20">
        {/* Top Bar */}
        <motion.header
          initial={{ y: -20, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
          transition={{ duration: 0.6, ease: 'easeOut' }}
          className="bg-white shadow-sm sticky top-0 z-30"
        >
          <div className="px-12 py-6 flex items-center justify-between">
            <div>
              <h1 className="font-serif text-3xl font-bold text-charcoal">
                {greeting}, {user.displayName || 'Designer'}
              </h1>
              <p className="text-text-secondary mt-1">Ready to create something extraordinary?</p>
            </div>
            
            <div className="flex items-center space-x-4">
              <div className="text-right">
                <p className="text-sm text-text-secondary">Design Credits</p>
                <p className="text-lg font-semibold text-gold">Unlimited</p>
              </div>
              <div className="w-12 h-12 bg-gradient-to-br from-purple-400 to-purple-600 rounded-full flex items-center justify-center">
                <UserIcon className="w-6 h-6 text-white" />
              </div>
            </div>
          </div>
        </motion.header>
        
        {/* Dashboard Content */}
        <div className="px-12 py-8">
          {/* Hero Section */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.2 }}
            className="mb-12"
          >
            <Card variant="elevated" className="bg-gradient-to-r from-gold/10 to-amber-50 border border-gold/20">
              <div className="flex items-center justify-between">
                <div className="flex-1">
                  <h2 className="font-serif text-4xl font-bold text-charcoal mb-4">
                    Create Your Next Interior Masterpiece
                  </h2>
                  <p className="text-xl text-text-secondary mb-6 max-w-2xl">
                    Transform your space with AI-powered designs that blend aesthetics, 
                    functionality, and Vastu principles for perfect harmony.
                  </p>
                  <Button
                    size="xl"
                    onClick={() => navigate('/upload')}
                    rightIcon={<ArrowRightIcon className="w-6 h-6" />}
                    className="px-8 py-4"
                  >
                    Start New Design
                  </Button>
                </div>
                
                <div className="hidden lg:block">
                  <div className="relative">
                    <div className="w-64 h-64 bg-gradient-to-br from-gold/20 to-amber-100 rounded-3xl flex items-center justify-center">
                      <SparklesIcon className="w-24 h-24 text-gold animate-pulse" />
                    </div>
                    <motion.div
                      animate={{ rotate: 360 }}
                      transition={{ duration: 20, repeat: Infinity, ease: 'linear' }}
                      className="absolute inset-0 w-64 h-64 border-2 border-gold/20 rounded-3xl"
                    />
                  </div>
                </div>
              </div>
            </Card>
          </motion.div>
          
          {/* Stats Grid */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.3 }}
            className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-12"
          >
            <Card className="text-center">
              <div className="w-16 h-16 bg-gradient-to-br from-blue-500 to-blue-600 rounded-2xl flex items-center justify-center mx-auto mb-4">
                <PhotoIcon className="w-8 h-8 text-white" />
              </div>
              <h3 className="text-3xl font-bold text-charcoal mb-1">{mockStats.totalDesigns}</h3>
              <p className="text-text-secondary mb-2">Total Designs</p>
              <p className="text-sm text-success">+{mockStats.thisMonth} this month</p>
            </Card>
            
            <Card className="text-center">
              <div className="w-16 h-16 bg-gradient-to-br from-green-500 to-green-600 rounded-2xl flex items-center justify-center mx-auto mb-4">
                <ArrowTrendingUpIcon className="w-8 h-8 text-white" />
              </div>
              <h3 className="text-3xl font-bold text-charcoal mb-1">${(mockStats.avgCost / 1000).toFixed(0)}k</h3>
              <p className="text-text-secondary mb-2">Avg. Project Value</p>
              <p className="text-sm text-success">Above average</p>
            </Card>
            
            <Card className="text-center">
              <div className="w-16 h-16 bg-gradient-to-br from-purple-500 to-purple-600 rounded-2xl flex items-center justify-center mx-auto mb-4">
                <SparklesIcon className="w-8 h-8 text-white" />
              </div>
              <h3 className="text-3xl font-bold text-charcoal mb-1">{mockStats.completionRate}%</h3>
              <p className="text-text-secondary mb-2">Completion Rate</p>
              <p className="text-sm text-success">Excellent</p>
            </Card>
            
            <Card className="text-center">
              <div className="w-16 h-16 bg-gradient-to-br from-gold to-amber-600 rounded-2xl flex items-center justify-center mx-auto mb-4">
                <HeartIcon className="w-8 h-8 text-white" />
              </div>
              <h3 className="text-xl font-bold text-charcoal mb-1">{mockStats.favoriteStyle}</h3>
              <p className="text-text-secondary mb-2">Favorite Style</p>
              <p className="text-sm text-gold">Most chosen</p>
            </Card>
          </motion.div>
          
          {/* Recent Designs */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.4 }}
          >
            <div className="flex items-center justify-between mb-8">
              <div>
                <h2 className="font-serif text-3xl font-bold text-charcoal mb-2">
                  Recent Designs
                </h2>
                <p className="text-text-secondary">
                  Your latest interior design creations
                </p>
              </div>
              <Button
                variant="outline"
                onClick={() => navigate('/history')}
                rightIcon={<EyeIcon className="w-5 h-5" />}
              >
                View All
              </Button>
            </div>
            
            {isLoading ? (
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
                {[1, 2, 3].map((i) => (
                  <div key={i} className="animate-pulse">
                    <div className="bg-gray-200 rounded-3xl aspect-[4/3] mb-4" />
                    <div className="h-4 bg-gray-200 rounded mb-2" />
                    <div className="h-3 bg-gray-200 rounded w-3/4" />
                  </div>
                ))}
              </div>
            ) : designs?.length ? (
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
                {designs.map((design, index) => (
                  <motion.div
                    key={design.id}
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: 0.5 + index * 0.1 }}
                  >
                    <DesignCard
                      title={design.title}
                      imageUrl={design.imageUrl}
                      style={design.style}
                      cost={design.cost}
                      onClick={() => navigate(`/design/${design.id}`)}
                    />
                  </motion.div>
                ))}
              </div>
            ) : (
              <Card className="text-center py-16">
                <div className="w-20 h-20 bg-gold/10 rounded-full flex items-center justify-center mx-auto mb-6">
                  <PhotoIcon className="w-10 h-10 text-gold" />
                </div>
                <h3 className="font-serif text-2xl font-bold text-charcoal mb-4">
                  No Designs Yet
                </h3>
                <p className="text-text-secondary mb-8 max-w-md mx-auto">
                  Start your interior design journey by uploading your room images and letting our AI create beautiful designs for you.
                </p>
                <Button
                  size="lg"
                  onClick={() => navigate('/upload')}
                  rightIcon={<ArrowRightIcon className="w-5 h-5" />}
                >
                  Create Your First Design
                </Button>
              </Card>
            )}
          </motion.div>
        </div>
      </div>
    </div>
  );
};

export default PremiumDashboard;
