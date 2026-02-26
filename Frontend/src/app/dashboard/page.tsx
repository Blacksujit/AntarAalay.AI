'use client';

import { useEffect, useMemo, useState } from 'react';
import { motion } from 'framer-motion';
import { 
  CompassIcon, 
  HomeIcon, 
  UploadIcon, 
  SparklesIcon,
  UserIcon,
  SettingsIcon,
  LogOutIcon,
  PlusIcon,
  ClockIcon,
  ArrowRightIcon,
  SmartphoneIcon
} from 'lucide-react';
import Link from 'next/link';
import { useRouter } from 'next/navigation';
import { dashboardService, debugDashboard, type Design } from '../../services/apiService';
import { useAuthStore } from '../../store/authStore';
import QRModal from '../../components/ar/QRModal';

export default function DashboardPage() {
  const router = useRouter();
  const { user, isAuthenticated, initializeAuth, logout } = useAuthStore();
  const [isLoading, setIsLoading] = useState(true);
  const [stats, setStats] = useState<{ totalDesigns: number; thisMonth: number; avgGenerationTime: number; favoriteStyle: string } | null>(null);
  const [recentDesigns, setRecentDesigns] = useState<Design[]>([]);
  const [showARModal, setShowARModal] = useState(false);

  // Debug function to test authentication and database
  const testDebugEndpoint = async () => {
    try {
      console.log('Testing debug endpoint...');
      const debugData = await debugDashboard();
      console.log('Debug data:', debugData);
      alert(`Debug Info:\nUser ID: ${debugData.user?.user_id}\nUser Email: ${debugData.user?.user_email}\nUser Designs: ${debugData.database?.user_designs_count}\nTotal DB Designs: ${debugData.database?.total_designs_in_db}`);
    } catch (error) {
      console.error('Debug test failed:', error);
      alert('Debug test failed. Check console for details.');
    }
  };
  const [selectedDesignId, setSelectedDesignId] = useState<string | null>(null);
  const displayName = useMemo(() => user?.displayName || user?.email || 'Designer', [user]);

  useEffect(() => {
    void initializeAuth();
  }, [initializeAuth]);

  useEffect(() => {
    if (isAuthenticated === false) {
      router.push('/login');
    }
  }, [isAuthenticated, router]);

  useEffect(() => {
    let cancelled = false;
    async function load() {
      try {
        setIsLoading(true);
        console.log('Loading dashboard data...');
        
        // Only try to load stats if user is authenticated
        if (user?.uid) {
          const resp = await dashboardService.getStats();
          if (cancelled) return;
          console.log('Dashboard data loaded:', resp);
          setStats(resp.stats);
          setRecentDesigns(resp.recentDesigns || []);
        } else {
          console.log('User not authenticated, skipping dashboard data load');
          setStats({
            totalDesigns: 0,
            thisMonth: 0,
            avgGenerationTime: 0,
            favoriteStyle: 'Modern'
          });
          setRecentDesigns([]);
        }
      } catch (error) {
        console.error('Failed to load dashboard data:', error);
        if (cancelled) return;
        
        // Set default values on error
        setStats({
          totalDesigns: 0,
          thisMonth: 0,
          avgGenerationTime: 0,
          favoriteStyle: 'Modern'
        });
        setRecentDesigns([]);
      } finally {
        if (!cancelled) setIsLoading(false);
      }
    }

    if (isAuthenticated) {
      load();
    } else {
      setIsLoading(false);
    }

    return () => {
      cancelled = true;
    };
  }, [isAuthenticated, user]);

  const handleLogout = async () => {
    await logout();
    router.push('/');
  };

  const handleARClick = () => {
    // Always allow AR access, even without authentication for demo purposes
    const designId = recentDesigns.length > 0 ? recentDesigns[0].id : 'demo-design-id';
    const roomId = recentDesigns.length > 0 ? recentDesigns[0].room_id : 'demo-room-id';
    const userId = user?.uid || 'demo-user';
    
    setSelectedDesignId(designId);
    setShowARModal(true);
    
    console.log('AR Session initiated:', { designId, roomId, userId, hasDesigns: recentDesigns.length > 0 });
  };

  return (
    <div className="min-h-screen bg-[#F4EFE6]">
      {/* Top Navigation */}
      <nav className="fixed top-0 left-0 right-0 z-50 bg-white/80 backdrop-blur-md border-b border-[#C6A75E]/20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            <Link href="/" className="flex items-center space-x-2">
              <CompassIcon className="w-8 h-8 text-[#C6A75E]" />
              <span className="text-xl font-bold text-[#1F1F1F]">AntarAalay.ai</span>
            </Link>

            <div className="flex items-center space-x-4">
              <Link href="/dashboard" className="p-2 text-[#C6A75E] rounded-lg bg-[#C6A75E]/10">
                <HomeIcon className="w-5 h-5" />
              </Link>
              <button 
                onClick={testDebugEndpoint} 
                className="p-2 text-[#1F1F1F] hover:text-blue-500 transition-colors"
                title="Debug Dashboard"
              >
                <SettingsIcon className="w-5 h-5" />
              </button>
              <Link href="/settings" className="p-2 text-[#1F1F1F] hover:text-[#C6A75E] transition-colors">
                <SettingsIcon className="w-5 h-5" />
              </Link>
              <button onClick={handleLogout} className="p-2 text-[#1F1F1F] hover:text-red-500 transition-colors">
                <LogOutIcon className="w-5 h-5" />
              </button>
              <div className="w-8 h-8 bg-[#C6A75E] rounded-full flex items-center justify-center text-white" title={displayName}>
                <UserIcon className="w-4 h-4" />
              </div>
            </div>
          </div>
        </div>
      </nav>

      {/* Main Content */}
      <main className="pt-24 pb-12 px-4 sm:px-6 lg:px-8">
        <div className="max-w-7xl mx-auto">
          {/* Welcome Section */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="mb-8"
          >
            <h1 className="text-3xl font-bold text-[#1F1F1F] mb-2">Welcome to Your Studio</h1>
            <p className="text-gray-600">
              Your space has an orientation. Your design has an intention. Let's align both.
            </p>
          </motion.div>

          {stats && (
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 mb-10">
              <div className="bg-white rounded-2xl p-5 shadow-lg border border-gray-100">
                <p className="text-sm text-gray-500">Total Designs</p>
                <p className="text-2xl font-bold text-[#1F1F1F] mt-1">{stats.totalDesigns}</p>
              </div>
              <div className="bg-white rounded-2xl p-5 shadow-lg border border-gray-100">
                <p className="text-sm text-gray-500">This Month</p>
                <p className="text-2xl font-bold text-[#1F1F1F] mt-1">{stats.thisMonth}</p>
              </div>
              <div className="bg-white rounded-2xl p-5 shadow-lg border border-gray-100">
                <p className="text-sm text-gray-500">Avg Generation</p>
                <p className="text-2xl font-bold text-[#1F1F1F] mt-1">{stats.avgGenerationTime}s</p>
              </div>
              <div className="bg-white rounded-2xl p-5 shadow-lg border border-gray-100">
                <p className="text-sm text-gray-500">Favorite Style</p>
                <p className="text-2xl font-bold text-[#1F1F1F] mt-1">{stats.favoriteStyle}</p>
              </div>
            </div>
          )}

          {/* Quick Actions */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-12">
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.1 }}
            >
              <Link href="/upload" className="block bg-white rounded-2xl p-6 shadow-lg hover:shadow-xl transition-all border border-gray-100 group">
                <div className="w-12 h-12 bg-[#C6A75E]/10 rounded-xl flex items-center justify-center mb-4 group-hover:bg-[#C6A75E]/20 transition-colors">
                  <UploadIcon className="w-6 h-6 text-[#C6A75E]" />
                </div>
                <h3 className="text-lg font-semibold text-[#1F1F1F] mb-2">Upload Room</h3>
                <p className="text-sm text-gray-600">Upload a photo of your space to get started</p>
              </Link>
            </motion.div>

            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.2 }}
            >
              <button 
                onClick={handleARClick}
                className="w-full bg-white rounded-2xl p-6 shadow-lg hover:shadow-xl transition-all border border-gray-100 group text-left"
              >
                <div className="w-12 h-12 bg-[#C6A75E]/10 rounded-xl flex items-center justify-center mb-4 group-hover:bg-[#C6A75E]/20 transition-colors">
                  <SmartphoneIcon className="w-6 h-6 text-[#C6A75E]" />
                </div>
                <h3 className="text-lg font-semibold text-[#1F1F1F] mb-2">Try in AR Vastu</h3>
                <p className="text-sm text-gray-600">Experience your design in mobile AR</p>
              </button>
            </motion.div>

            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.3 }}
            >
              <Link href="/compass" className="block bg-white rounded-2xl p-6 shadow-lg hover:shadow-xl transition-all border border-gray-100 group">
                <div className="w-12 h-12 bg-[#C6A75E]/10 rounded-xl flex items-center justify-center mb-4 group-hover:bg-[#C6A75E]/20 transition-colors">
                  <CompassIcon className="w-6 h-6 text-[#C6A75E]" />
                </div>
                <h3 className="text-lg font-semibold text-[#1F1F1F] mb-2">Spatial Harmony</h3>
                <p className="text-sm text-gray-600">Align your space with energy and direction</p>
              </Link>
            </motion.div>
          </div>

          {/* Recent Designs */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.4 }}
            className="bg-white rounded-2xl shadow-lg border border-gray-100"
          >
            <div className="p-6 border-b border-gray-100 flex items-center justify-between">
              <h2 className="text-xl font-bold text-[#1F1F1F]">Recent Designs</h2>
              <Link href="/designs" className="text-[#C6A75E] hover:text-[#B89A4F] text-sm font-medium">
                View All
              </Link>
            </div>

            <div className="divide-y divide-gray-100">
              {isLoading && (
                <div className="p-6 text-gray-500">Loading your designs...</div>
              )}

              {!isLoading && recentDesigns.length === 0 && (
                <div className="p-6 text-gray-500">
                  No designs yet. Upload your room images to begin.
                </div>
              )}

              {recentDesigns.map((design) => (
                <div key={design.id} className="p-6 flex items-center justify-between hover:bg-gray-50 transition-colors">
                  <div className="flex items-center space-x-4">
                    <div className="w-16 h-16 bg-[#F4EFE6] rounded-xl flex items-center justify-center">
                      <HomeIcon className="w-8 h-8 text-[#C6A75E]" />
                    </div>
                    <div>
                      <h3 className="font-semibold text-[#1F1F1F]">{design.style}</h3>
                      <div className="flex items-center text-sm text-gray-500 mt-1">
                        <ClockIcon className="w-4 h-4 mr-1" />
                        {new Date(design.created_at).toLocaleString()}
                      </div>
                    </div>
                  </div>
                  <div className="flex items-center space-x-3">
                    <span className={`px-3 py-1 rounded-full text-xs font-medium ${
                      design.status === 'completed' 
                        ? 'bg-green-100 text-green-700' 
                        : 'bg-amber-100 text-amber-700'
                    }`}>
                      {design.status}
                    </span>
                    <Link href={`/designs/${design.id}`} className="p-2 text-gray-400 hover:text-[#C6A75E] transition-colors">
                      <ArrowRightIcon className="w-5 h-5" />
                    </Link>
                  </div>
                </div>
              ))}
            </div>
          </motion.div>
        </div>
      </main>

      {/* AR QR Modal */}
      {showARModal && (
        <QRModal
          isOpen={showARModal}
          onClose={() => setShowARModal(false)}
          designId={selectedDesignId || 'demo-design-id'}
          roomId={recentDesigns.length > 0 ? recentDesigns[0]?.room_id || 'demo-room-id' : 'demo-room-id'}
          userId={user?.uid || 'demo-user'}
        />
      )}
    </div>
  );
}
