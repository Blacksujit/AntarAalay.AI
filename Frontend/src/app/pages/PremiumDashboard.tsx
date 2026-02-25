/**
 * Premium Dashboard
 * AntarAalay.ai - Luxury Interior Design Dashboard
 */

import { useState } from 'react';
import { motion } from 'framer-motion';
import { useNavigate } from 'react-router-dom';
import { 
  HomeIcon, 
  PhotoIcon, 
  ArrowTrendingUpIcon,
  UserIcon,
  PlusIcon,
  SparklesIcon,
  EyeIcon,
  HeartIcon,
  CameraIcon,
  ClockIcon
} from '@heroicons/react/24/outline';
import { useQuery } from '@tanstack/react-query';
import { useAuthStore } from '../../store/authStore';
import { PremiumButton, GlassCard, DesignCard } from '../../components/ui/PremiumComponents';

// Mock data for demonstration
const mockDesigns = [
  {
    id: '1',
    title: 'Modern Living Room',
    imageUrl: 'https://images.unsplash.com/photo-1586023492125-27b2c045efd7?w=400&h=300&fit=crop',
    style: 'Contemporary',
    cost: '$45,000',
    roomType: 'Living Room',
    createdAt: '2024-01-15',
  },
  {
    id: '2',
    title: 'Minimalist Bedroom',
    imageUrl: 'https://images.unsplash.com/photo-1560185007-c5ca9d2c014d?w=400&h=300&fit=crop',
    style: 'Minimalist',
    cost: '$32,000',
    roomType: 'Bedroom',
    createdAt: '2024-01-14',
  },
  {
    id: '3',
    title: 'Luxury Kitchen',
    imageUrl: 'https://images.unsplash.com/photo-1556909114-f6e7ad7d3136?w=400&h=300&fit=crop',
    style: 'Modern',
    cost: '$65,000',
    roomType: 'Kitchen',
    createdAt: '2024-01-13',
  },
];

interface DashboardStats {
  totalDesigns: number;
  thisMonth: number;
  avgCost: number;
  favoriteStyle: string;
  vastuScore: number;
}

export const PremiumDashboard: React.FC = () => {
  const navigate = useNavigate();
  const { user } = useAuthStore();
  const [stats] = useState<DashboardStats>({
    totalDesigns: 12,
    thisMonth: 3,
    avgCost: 42000,
    favoriteStyle: 'Contemporary',
    vastuScore: 85,
  });

  // Mock API call for user's designs
  const { data: userDesigns, isLoading } = useQuery({
    queryKey: ['userDesigns'],
    queryFn: () => Promise.resolve(mockDesigns),
    staleTime: 5 * 60 * 1000,
  });

  const statCards = [
    {
      title: 'Total Designs',
      value: stats.totalDesigns,
      change: `+${stats.thisMonth} this month`,
      icon: PhotoIcon,
      color: 'from-blue-500 to-blue-600',
      trend: 'up',
    },
    {
      title: 'Average Cost',
      value: `$${(stats.avgCost / 1000).toFixed(0)}k`,
      change: 'Within budget',
      icon: ArrowTrendingUpIcon,
      color: 'from-green-500 to-green-600',
      trend: 'stable',
    },
    {
      title: 'Vastu Score',
      value: `${stats.vastuScore}%`,
      change: 'Excellent harmony',
      icon: SparklesIcon,
      color: 'from-purple-500 to-purple-600',
      trend: 'up',
    },
    {
      title: 'Favorite Style',
      value: stats.favoriteStyle,
      change: 'Most chosen',
      icon: HeartIcon,
      color: 'from-pink-500 to-pink-600',
      trend: 'stable',
    },
  ];

  if (!user) {
    navigate('/login');
    return null;
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-amber-50 via-orange-50 to-rose-50">
      {/* Header */}
      <motion.header
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        className="bg-white/80 backdrop-blur-lg border-b border-amber-100 sticky top-0 z-50"
      >
        <div className="max-w-7xl mx-auto px-6 py-6">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-4">
              <div className="w-12 h-12 bg-gradient-to-br from-amber-400 to-amber-600 rounded-xl flex items-center justify-center shadow-glow">
                <HomeIcon className="w-6 h-6 text-white" />
              </div>
              <div>
                <h1 className="text-2xl font-serif font-bold text-gray-900">Design Studio</h1>
                <p className="text-gray-600">Welcome back, {user.displayName || 'Designer'}</p>
              </div>
            </div>
            
            <div className="flex items-center space-x-4">
              <PremiumButton
                variant="outline"
                leftIcon={<PlusIcon className="w-4 h-4" />}
                onClick={() => navigate('/upload')}
              >
                New Design
              </PremiumButton>
              
              <div className="w-10 h-10 bg-gradient-to-br from-purple-400 to-purple-600 rounded-full flex items-center justify-center cursor-pointer">
                <UserIcon className="w-5 h-5 text-white" />
              </div>
            </div>
          </div>
        </div>
      </motion.header>

      {/* Main Content */}
      <div className="max-w-7xl mx-auto px-6 py-12">
        {/* Quick Actions */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
          className="mb-12"
        >
          <GlassCard className="bg-gradient-to-r from-amber-100 to-orange-100 border-amber-200">
            <div className="flex items-center justify-between">
              <div>
                <h2 className="text-xl font-serif font-bold text-gray-900 mb-2">
                  Ready to Transform Your Space?
                </h2>
                <p className="text-gray-700">
                  Upload your room images and let AI create stunning designs tailored to your style.
                </p>
              </div>
              <PremiumButton
                size="lg"
                leftIcon={<PlusIcon className="w-5 h-5" />}
                onClick={() => navigate('/upload')}
              >
                Start New Design
              </PremiumButton>
            </div>
          </GlassCard>
        </motion.div>

        {/* Stats Grid */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
          className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-12"
        >
          {statCards.map((stat, index) => (
            <motion.div
              key={stat.title}
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ delay: 0.3 + index * 0.1 }}
            >
              <GlassCard className="text-center">
                <div className={`w-12 h-12 bg-gradient-to-br ${stat.color} rounded-xl flex items-center justify-center mx-auto mb-4`}>
                  <stat.icon className="w-6 h-6 text-white" />
                </div>
                <h3 className="text-2xl font-bold text-gray-900 mb-1">{stat.value}</h3>
                <p className="text-sm font-medium text-gray-600 mb-2">{stat.title}</p>
                <p className="text-xs text-gray-500">{stat.change}</p>
              </GlassCard>
            </motion.div>
          ))}
        </motion.div>

        {/* Recent Designs */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.4 }}
        >
          <div className="flex items-center justify-between mb-8">
            <div>
              <h2 className="text-2xl font-serif font-bold text-gray-900 mb-2">
                Recent Designs
              </h2>
              <p className="text-gray-600">
                Your latest interior design creations
              </p>
            </div>
            <PremiumButton
              variant="outline"
              rightIcon={<EyeIcon className="w-4 h-4" />}
              onClick={() => navigate('/history')}
            >
              View All
            </PremiumButton>
          </div>

          {isLoading ? (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
              {[1, 2, 3].map((i) => (
                <div key={i} className="animate-pulse">
                  <div className="bg-gray-200 rounded-2xl aspect-[4/3] mb-4" />
                  <div className="h-4 bg-gray-200 rounded mb-2" />
                  <div className="h-3 bg-gray-200 rounded w-3/4" />
                </div>
              ))}
            </div>
          ) : userDesigns?.length ? (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
              {userDesigns.map((design, index) => (
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
            <GlassCard className="text-center py-16">
              <div className="w-20 h-20 bg-amber-100 rounded-full flex items-center justify-center mx-auto mb-6">
                <PhotoIcon className="w-10 h-10 text-amber-600" />
              </div>
              <h3 className="text-xl font-serif font-bold text-gray-900 mb-4">
                No Designs Yet
              </h3>
              <p className="text-gray-600 mb-8 max-w-md mx-auto">
                Start your interior design journey by uploading your room images and letting our AI create beautiful designs for you.
              </p>
              <PremiumButton
                size="lg"
                leftIcon={<PlusIcon className="w-5 h-5" />}
                onClick={() => navigate('/upload')}
              >
                Create Your First Design
              </PremiumButton>
            </GlassCard>
          )}
        </motion.div>

        {/* Quick Tips */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.6 }}
          className="mt-16"
        >
          <GlassCard className="bg-gradient-to-r from-purple-50 to-pink-50 border-purple-200">
            <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
              <div className="text-center">
                <div className="w-12 h-12 bg-purple-100 rounded-xl flex items-center justify-center mx-auto mb-4">
                  <CameraIcon className="w-6 h-6 text-purple-600" />
                </div>
                <h3 className="font-semibold text-gray-900 mb-2">Capture All Angles</h3>
                <p className="text-sm text-gray-600">
                  Photograph your room from all four directions for best results
                </p>
              </div>
              
              <div className="text-center">
                <div className="w-12 h-12 bg-pink-100 rounded-xl flex items-center justify-center mx-auto mb-4">
                  <SparklesIcon className="w-6 h-6 text-pink-600" />
                </div>
                <h3 className="font-semibold text-gray-900 mb-2">Vastu Compliant</h3>
                <p className="text-sm text-gray-600">
                  All designs follow Vastu principles for harmony and prosperity
                </p>
              </div>
              
              <div className="text-center">
                <div className="w-12 h-12 bg-amber-100 rounded-xl flex items-center justify-center mx-auto mb-4">
                  <ClockIcon className="w-6 h-6 text-amber-600" />
                </div>
                <h3 className="font-semibold text-gray-900 mb-2">Quick Results</h3>
                <p className="text-sm text-gray-600">
                  Get 3 design variations in under 60 seconds with cost estimates
                </p>
              </div>
            </div>
          </GlassCard>
        </motion.div>
      </div>
    </div>
  );
};

export default PremiumDashboard;
