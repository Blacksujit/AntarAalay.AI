/**
 * Enterprise Dashboard
 * Premium overview with stats cards and recent designs
 */

import { useEffect, useState } from 'react';
import { motion } from 'framer-motion';
import { useNavigate } from 'react-router-dom';
import { 
  SparklesIcon,
  PhotoIcon,
  ArrowTrendingUpIcon,
  ClockIcon,
  PlusIcon,
  ChevronRightIcon
} from '@heroicons/react/24/outline';
import { Card, CardContent } from '../../components/ui/Card';
import { Button } from '../../components/ui/Button';
import { LoadingSpinner, CardSkeleton } from '../../components/ui/Loading';
import { dashboardService, type DashboardStats, type Design } from '../../services/apiService';
import { useGlobalStore, selectRemainingGenerations, selectCanGenerate } from '../../store/globalStore';
import { cn } from '../../utils/logger';

const StatCard = ({ 
  icon: Icon, 
  label, 
  value, 
  trend,
  delay 
}: { 
  icon: React.ElementType; 
  label: string; 
  value: string | number;
  trend?: string;
  delay: number;
}) => (
  <motion.div
    initial={{ opacity: 0, y: 30 }}
    animate={{ opacity: 1, y: 0 }}
    transition={{ delay, duration: 0.6 }}
  >
    <Card className="h-full">
      <CardContent className="p-6">
        <div className="flex items-start justify-between">
          <div className="p-3 bg-brand-gold/10 rounded-xl">
            <Icon className="w-6 h-6 text-brand-gold" />
          </div>
          {trend && (
            <span className="text-sm text-green-600 font-medium bg-green-50 px-2 py-1 rounded-full">
              {trend}
            </span>
          )}
        </div>
        <div className="mt-4">
          <p className="text-3xl font-display font-bold text-brand-charcoal">
            {value}
          </p>
          <p className="text-sm text-neutral-500 mt-1">{label}</p>
        </div>
      </CardContent>
    </Card>
  </motion.div>
);

export const Dashboard = () => {
  const navigate = useNavigate();
  const [stats, setStats] = useState<DashboardStats | null>(null);
  const [recentDesigns, setRecentDesigns] = useState<Design[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  
  const remainingGenerations = useGlobalStore(selectRemainingGenerations);
  const canGenerate = useGlobalStore(selectCanGenerate);

  useEffect(() => {
    const fetchDashboardData = async () => {
      try {
        const response = await dashboardService.getStats();
        setStats(response.stats);
        setRecentDesigns(response.recentDesigns);
      } catch (error) {
        console.error('Failed to fetch dashboard data:', error);
      } finally {
        setIsLoading(false);
      }
    };

    fetchDashboardData();
  }, []);

  if (isLoading) {
    return (
      <div className="space-y-8">
        <div className="h-8 w-48 bg-neutral-200 rounded animate-pulse" />
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {[...Array(4)].map((_, i) => (
            <CardSkeleton key={i} />
          ))}
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-8">
      {/* Welcome Header */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="flex flex-col md:flex-row md:items-center md:justify-between gap-4"
      >
        <div>
          <h1 className="text-3xl md:text-4xl font-display font-bold text-brand-charcoal">
            Welcome back, Designer
          </h1>
          <p className="text-neutral-600 mt-2">
            Transform your space with AI-powered interior design
          </p>
        </div>
        
        <Button
          size="lg"
          onClick={() => navigate('/upload')}
          disabled={!canGenerate}
          leftIcon={<PlusIcon className="w-5 h-5" />}
        >
          {!canGenerate ? 'Limit Reached' : 'New Design'}
        </Button>
      </motion.div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <StatCard
          icon={SparklesIcon}
          label="Total Designs"
          value={stats?.totalDesigns || 0}
          trend="+12%"
          delay={0}
        />
        <StatCard
          icon={PhotoIcon}
          label="This Month"
          value={stats?.thisMonth || 0}
          delay={0.1}
        />
        <StatCard
          icon={ClockIcon}
          label="Avg. Generation"
          value={`${stats?.avgGenerationTime || 45}s`}
          delay={0.2}
        />
        <StatCard
          icon={ArrowTrendingUpIcon}
          label="Top Style"
          value={stats?.favoriteStyle || 'Modern'}
          delay={0.3}
        />
      </div>

      {/* Quick Actions & Usage */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Quick Actions */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.4 }}
          className="lg:col-span-2"
        >
          <Card>
            <CardContent className="p-6">
              <h2 className="text-xl font-display font-bold text-brand-charcoal mb-4">
                Quick Actions
              </h2>
              <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                {[
                  { 
                    icon: PlusIcon, 
                    label: 'New Design', 
                    color: 'bg-brand-gold',
                    onClick: () => navigate('/upload'),
                    disabled: !canGenerate
                  },
                  { 
                    icon: PhotoIcon, 
                    label: 'My Designs', 
                    color: 'bg-blue-500',
                    onClick: () => navigate('/history')
                  },
                  { 
                    icon: ArrowTrendingUpIcon, 
                    label: 'Compare', 
                    color: 'bg-purple-500',
                    onClick: () => navigate('/compare')
                  },
                  { 
                    icon: SparklesIcon, 
                    label: 'Vastu Tips', 
                    color: 'bg-green-500',
                    onClick: () => navigate('/vastu')
                  },
                ].map((action, i) => (
                  <motion.button
                    key={i}
                    whileHover={{ scale: 1.05 }}
                    whileTap={{ scale: 0.95 }}
                    onClick={action.onClick}
                    disabled={action.disabled}
                    className={cn(
                      'flex flex-col items-center gap-3 p-4 rounded-xl transition-all duration-300',
                      'hover:shadow-soft disabled:opacity-50 disabled:cursor-not-allowed'
                    )}
                  >
                    <div className={cn('w-12 h-12 rounded-xl flex items-center justify-center text-white', action.color)}>
                      <action.icon className="w-6 h-6" />
                    </div>
                    <span className="text-sm font-medium text-brand-charcoal">
                      {action.label}
                    </span>
                  </motion.button>
                ))}
              </div>
            </CardContent>
          </Card>
        </motion.div>

        {/* Usage Card */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.5 }}
        >
          <Card className="h-full bg-gradient-to-br from-brand-gold/10 to-brand-gold/5 border-brand-gold/20">
            <CardContent className="p-6 flex flex-col justify-between h-full">
              <div>
                <h3 className="text-lg font-display font-bold text-brand-charcoal mb-2">
                  Daily Usage
                </h3>
                <p className="text-sm text-neutral-600">
                  {remainingGenerations} of 3 designs remaining today
                </p>
              </div>
              
              <div className="mt-6">
                <div className="flex justify-between text-sm mb-2">
                  <span className="text-neutral-600">Progress</span>
                  <span className="font-semibold text-brand-gold">
                    {Math.round((remainingGenerations / 3) * 100)}%
                  </span>
                </div>
                <div className="h-3 bg-white/50 rounded-full overflow-hidden">
                  <motion.div
                    initial={{ width: 0 }}
                    animate={{ width: `${(remainingGenerations / 3) * 100}%` }}
                    transition={{ duration: 0.8, delay: 0.6 }}
                    className="h-full bg-brand-gold rounded-full"
                  />
                </div>
                
                {remainingGenerations === 0 && (
                  <p className="text-sm text-red-600 mt-3">
                    You've reached your daily limit. Upgrade for unlimited designs.
                  </p>
                )}
              </div>
            </CardContent>
          </Card>
        </motion.div>
      </div>

      {/* Recent Designs */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.6 }}
      >
        <div className="flex items-center justify-between mb-6">
          <h2 className="text-2xl font-display font-bold text-brand-charcoal">
            Recent Designs
          </h2>
          <Button
            variant="ghost"
            onClick={() => navigate('/history')}
            rightIcon={<ChevronRightIcon className="w-4 h-4" />}
          >
            View All
          </Button>
        </div>

        {recentDesigns.length > 0 ? (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {recentDesigns.slice(0, 6).map((design, index) => (
              <motion.div
                key={design.id}
                initial={{ opacity: 0, scale: 0.9 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ delay: index * 0.1 }}
                whileHover={{ y: -4 }}
                onClick={() => navigate(`/design/${design.id}`)}
                className="cursor-pointer"
              >
                <Card className="overflow-hidden">
                  <div className="aspect-video bg-neutral-100 relative">
                    {design.image_1_url ? (
                      <img
                        src={design.image_1_url}
                        alt={`${design.style} design`}
                        className="w-full h-full object-cover"
                      />
                    ) : (
                      <div className="w-full h-full flex items-center justify-center">
                        <PhotoIcon className="w-12 h-12 text-neutral-300" />
                      </div>
                    )}
                    
                    {/* Style Badge */}
                    <div className="absolute top-3 left-3 px-3 py-1 bg-white/90 backdrop-blur-sm rounded-full text-xs font-medium text-brand-charcoal">
                      {design.style}
                    </div>
                    
                    {/* Vastu Score */}
                    {design.vastu_score && (
                      <div className="absolute top-3 right-3 px-3 py-1 bg-green-500/90 backdrop-blur-sm rounded-full text-xs font-medium text-white">
                        Vastu: {design.vastu_score}%
                      </div>
                    )}
                  </div>
                  
                  <CardContent className="p-4">
                    <div className="flex items-center justify-between">
                      <div>
                        <p className="font-medium text-brand-char capitalize">
                          {design.style} Interior
                        </p>
                        <p className="text-sm text-neutral-500">
                          {new Date(design.created_at).toLocaleDateString()}
                        </p>
                      </div>
                      {design.estimated_cost && (
                        <p className="text-lg font-semibold text-brand-gold">
                          ₹{design.estimated_cost.toLocaleString()}
                        </p>
                      )}
                    </div>
                  </CardContent>
                </Card>
              </motion.div>
            ))}
          </div>
        ) : (
          <Card className="py-16 text-center">
            <PhotoIcon className="w-16 h-16 mx-auto text-neutral-300 mb-4" />
            <h3 className="text-xl font-display font-bold text-brand-charcoal mb-2">
              No designs yet
            </h3>
            <p className="text-neutral-600 mb-6">
              Start by uploading your room to create stunning AI designs
            </p>
            <Button onClick={() => navigate('/upload')}>
              Create Your First Design
            </Button>
          </Card>
        )}
      </motion.div>
    </div>
  );
};

export default Dashboard;
