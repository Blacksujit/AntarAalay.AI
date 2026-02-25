/**
 * Premium Dashboard for AntarAalay.ai
 * Enterprise-grade interior design management
 */

import { useState, useEffect, useRef } from 'react';
import { motion } from 'framer-motion';
import { 
  HomeIcon, 
  PhotoIcon, 
  ArrowTrendingUpIcon,
  UserIcon,
  Cog6ToothIcon,
  PlusIcon
} from '@heroicons/react/24/outline';
import { cn } from '../utils/logger';
import { useNavigate, Link } from 'react-router-dom';
import { useQuery } from '@tanstack/react-query';
import { useAuthStore } from '../store/authStore';
import { getUserRooms } from '../services/upload';

interface DashboardStats {
  totalDesigns: number;
  thisMonth: number;
  avgGenerationTime: number;
  favoriteStyle: string;
}

const Dashboard = () => {
  const navigate = useNavigate();
  const { user, logout } = useAuthStore();
  const [authFailed, setAuthFailed] = useState(false);

  const [stats, setStats] = useState<DashboardStats>({
    totalDesigns: 0,
    thisMonth: 0,
    avgGenerationTime: 45,
    favoriteStyle: 'modern',
  });

  // Only redirect if user was previously logged in and now is null
  const hasCheckedAuth = useRef(false);
  
  useEffect(() => {
    if (!hasCheckedAuth.current && !user) {
      hasCheckedAuth.current = true;
      navigate('/login');
    }
  }, [user, navigate]);

  // Redirect to login when auth fails (401)
  useEffect(() => {
    if (authFailed) {
      navigate('/login');
    }
  }, [authFailed, navigate]);

  const { data: roomsData, isLoading } = useQuery({
    queryKey: ['userRooms'],
    queryFn: getUserRooms,
    enabled: !!user && !authFailed,
    retry: 0,
    staleTime: 5 * 60 * 1000,
    refetchOnWindowFocus: false,
    meta: {
      onError: (error: any) => {
        if (error?.response?.status === 401) {
          setAuthFailed(true);
        }
      },
    },
  });

  useEffect(() => {
    // Fetch dashboard stats
    const fetchDashboardStats = async () => {
      try {
        const response = await fetch('/api/dashboard/stats', {
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('auth_token')}`,
          },
        });
        const data = await response.json();
        if (data.stats) {
          setStats(data.stats);
        }
      } catch (error) {
        console.error('Failed to fetch dashboard stats:', error);
      }
    };

    if (user && !authFailed) {
      fetchDashboardStats();
    }
  }, [user, authFailed]);

  const menuItems = [
    { icon: HomeIcon, label: 'Dashboard', active: true, href: '/dashboard' },
    { icon: PhotoIcon, label: 'Upload Room', active: false, href: '/upload' },
    { icon: ArrowTrendingUpIcon, label: 'My Designs', active: false, href: '/designs' },
    { icon: PlusIcon, label: 'Create New', active: false, href: '/upload' },
    { icon: UserIcon, label: 'Profile', active: false, href: '/profile' },
  ];

  const handleLogout = async () => {
    await logout();
    navigate('/');
  };

  const recentRooms = roomsData?.rooms?.slice(0, 6) || [];

  return (
    <div className="min-h-screen bg-gradient-to-br from-brand-beige via-white to-brand-white">
      <div className="flex">
        {/* Sidebar */}
        <motion.div
          initial={{ opacity: 0, x: -100 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ duration: 0.6 }}
          className="w-80 bg-brand-charcoal text-white min-h-screen shadow-luxury"
        >
          {/* Logo */}
          <div className="p-8 mb-8">
            <div className="flex items-center space-x-3">
              <div className="w-10 h-10 bg-brand-gold rounded-xl flex items-center justify-center">
                <span className="text-brand-charcoal font-bold text-lg">A</span>
              </div>
              <span className="text-2xl font-display font-bold">AntarAalay</span>
            </div>
          </div>

          {/* Navigation */}
          <nav className="px-4">
            <div className="space-y-2">
              {menuItems.map((item) => (
                <Link
                  key={item.label}
                  to={item.href}
                  className={cn(
                    "flex items-center space-x-3 px-4 py-3 rounded-xl transition-all duration-200",
                    item.active
                      ? "bg-brand-gold text-brand-charcoal"
                      : "text-neutral-400 hover:text-white hover:bg-neutral-800"
                  )}
                >
                  <item.icon className="w-5 h-5" />
                  <span className="font-medium">{item.label}</span>
                </Link>
              ))}
            </div>
          </nav>

          {/* Usage Counter */}
          <div className="absolute bottom-8 left-4 right-4 p-4 bg-neutral-900 rounded-xl">
            <div className="text-center">
              <div className="text-2xl font-bold text-brand-gold mb-2">
                {stats.totalDesigns}
              </div>
              <div className="text-xs text-neutral-400">
                Designs Generated
              </div>
            </div>
          </div>
        </motion.div>

        {/* Main Content */}
        <div className="flex-1">
          {/* Top Bar */}
          <motion.div
            initial={{ opacity: 0, y: -20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
            className="bg-white shadow-soft px-8 py-4 mb-8"
          >
            <div className="flex items-center justify-between">
              <div>
                <h1 className="text-3xl font-display font-bold text-brand-charcoal">
                  Design Dashboard
                </h1>
                <p className="text-neutral-600 font-body">
                  Welcome back to your interior design studio
                </p>
              </div>
              
              <div className="flex items-center space-x-4">
                <button className="p-2 rounded-lg hover:bg-neutral-100 transition-colors duration-200">
                  <Cog6ToothIcon className="w-5 h-5 text-neutral-600" />
                </button>
                <div className="flex items-center space-x-2 px-4 py-2 bg-brand-gold/10 rounded-lg">
                  <span className="text-sm font-medium text-brand-charcoal">Usage: </span>
                  <span className="text-brand-gold font-bold">Premium</span>
                </div>
              </div>
            </div>
          </motion.div>

          {/* Stats Cards */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
            <motion.div
              initial={{ opacity: 0, y: 30 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.8 }}
              className="bg-white rounded-2xl shadow-soft p-6 hover:shadow-luxury transition-all duration-300"
            >
              <div className="flex items-center justify-between mb-4">
                <h3 className="text-lg font-semibold text-brand-charcoal">Total Designs</h3>
                <PhotoIcon className="w-5 h-5 text-brand-gold" />
              </div>
              <div className="text-3xl font-bold text-brand-charcoal">
                {stats.totalDesigns}
              </div>
              <div className="text-sm text-neutral-500">
                All time projects
              </div>
            </motion.div>

            <motion.div
              initial={{ opacity: 0, y: 30 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.1, duration: 0.8 }}
              className="bg-white rounded-2xl shadow-soft p-6 hover:shadow-luxury transition-all duration-300"
            >
              <div className="flex items-center justify-between mb-4">
                <h3 className="text-lg font-semibold text-brand-charcoal">This Month</h3>
                <ArrowTrendingUpIcon className="w-5 h-5 text-brand-gold" />
              </div>
              <div className="text-3xl font-bold text-brand-charcoal">
                {stats.thisMonth}
              </div>
              <div className="text-sm text-neutral-500">
                New designs
              </div>
            </motion.div>

            <motion.div
              initial={{ opacity: 0, y: 30 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.2, duration: 0.8 }}
              className="bg-white rounded-2xl shadow-soft p-6 hover:shadow-luxury transition-all duration-300"
            >
              <div className="flex items-center justify-between mb-4">
                <h3 className="text-lg font-semibold text-brand-charcoal">Avg Time</h3>
                <div className="w-5 h-5 rounded-full bg-brand-gold/20 flex items-center justify-center">
                  <span className="text-xs font-bold text-brand-gold">45s</span>
                </div>
              </div>
              <div className="text-3xl font-bold text-brand-charcoal">
                {stats.avgGenerationTime}s
              </div>
              <div className="text-sm text-neutral-500">
                Generation time
              </div>
            </motion.div>

            <motion.div
              initial={{ opacity: 0, y: 30 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.3, duration: 0.8 }}
              className="bg-white rounded-2xl shadow-soft p-6 hover:shadow-luxury transition-all duration-300"
            >
              <div className="flex items-center justify-between mb-4">
                <h3 className="text-lg font-semibold text-brand-charcoal">Top Style</h3>
                <div className="px-3 py-1 bg-brand-gold/10 rounded-full">
                  <span className="text-sm font-bold text-brand-gold capitalize">
                    {stats.favoriteStyle}
                  </span>
                </div>
              </div>
              <div className="text-lg font-medium text-brand-charcoal capitalize">
                {stats.favoriteStyle === 'modern' && 'Modern Minimalist'}
                {stats.favoriteStyle === 'luxury' && 'Luxury Elegant'}
                {stats.favoriteStyle === 'traditional' && 'Classic Traditional'}
              </div>
            </motion.div>
          </div>

          {/* Recent Designs Grid */}
          <motion.div
            initial={{ opacity: 0, y: 50 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.4, duration: 0.8 }}
            className="mb-8"
          >
            <div className="flex items-center justify-between mb-6">
              <h2 className="text-2xl font-display font-bold text-brand-charcoal">
                Recent Designs
              </h2>
              <motion.button
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                onClick={() => navigate('/upload')}
                className="flex items-center space-x-2 px-6 py-3 bg-brand-gold text-white rounded-xl shadow-soft hover:shadow-glow transition-all duration-200"
              >
                <PlusIcon className="w-5 h-5" />
                <span className="font-medium">Create New Design</span>
              </motion.button>
            </div>

            {isLoading ? (
              <div className="flex justify-center items-center py-16">
                <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-brand-gold"></div>
              </div>
            ) : recentRooms.length > 0 ? (
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {recentRooms.map((room: any, index: number) => (
                  <motion.div
                    key={room.id || index}
                    initial={{ opacity: 0, scale: 0.9 }}
                    animate={{ opacity: 1, scale: 1 }}
                    transition={{ delay: index * 0.1, duration: 0.6 }}
                    whileHover={{ scale: 1.03, boxShadow: "0 10px 30px rgba(0, 0, 0, 0.15)" }}
                    className="bg-white rounded-2xl shadow-soft overflow-hidden cursor-pointer"
                    onClick={() => navigate(`/designs/${room.id}`)}
                  >
                    <div className="aspect-video bg-neutral-100">
                      <img
                        src={room.image_url || '/placeholder-room.jpg'}
                        alt={`Room ${room.id}`}
                        className="w-full h-full object-cover"
                      />
                    </div>
                    <div className="p-6">
                      <div className="flex items-center justify-between mb-2">
                        <h3 className="text-lg font-semibold text-brand-charcoal capitalize">
                          {room.room_type || 'Living Room'} Design
                        </h3>
                        <span className="text-xs px-2 py-1 bg-brand-gold/20 rounded-full text-brand-gold">
                          {room.direction || 'North'}
                        </span>
                      </div>
                      <p className="text-sm text-neutral-600 mb-3">
                        Created {new Date(room.created_at || Date.now()).toLocaleDateString()}
                      </p>
                      <div className="flex items-center justify-between">
                        <span className="text-lg font-bold text-brand-gold">
                          View Design
                        </span>
                        <span className="text-sm text-neutral-500">
                          →
                        </span>
                      </div>
                    </div>
                  </motion.div>
                ))}
              </div>
            ) : (
              <div className="text-center py-16">
                <PhotoIcon className="w-16 h-16 mx-auto text-neutral-300 mb-4" />
                <h3 className="text-xl font-semibold text-brand-charcoal mb-2">
                  No designs yet
                </h3>
                <p className="text-neutral-600 mb-6">
                  Upload your first room to get started with AI-powered interior design
                </p>
                <motion.button
                  whileHover={{ scale: 1.05, boxShadow: "0 0 30px rgba(198, 167, 94, 0.4)" }}
                  whileTap={{ scale: 0.95 }}
                  onClick={() => navigate('/upload')}
                  className="px-8 py-4 bg-brand-gold text-white rounded-xl shadow-luxury hover:shadow-glow transition-all duration-200"
                >
                  <PlusIcon className="w-5 h-5 mr-3" />
                  Upload Your First Room
                </motion.button>
              </div>
            )}
          </motion.div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;

export async function getServerSideProps() {
  return { props: {} };
}
