import { useEffect, useRef, useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useQuery } from '@tanstack/react-query';
import { useAuthStore } from '../store/authStore';
import { getUserRooms } from '../services/upload';
import { Plus, Image, Sparkles, ChevronRight, LogOut } from 'lucide-react';

export default function Dashboard() {
  const navigate = useNavigate();
  const { user, logout } = useAuthStore();
  const [authFailed, setAuthFailed] = useState(false);

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
          // Clear auth state on 401
          localStorage.removeItem('auth_token');
          // Redirect to login
          window.location.href = '/login';
        }
      },
    },
  });

  const handleLogout = async () => {
    await logout();
    navigate('/');
  };

  const recentRooms = roomsData?.rooms?.slice(0, 6) || [];

  return (
    <div className="min-h-screen bg-gradient-to-br from-amber-50 via-orange-50 to-rose-50">
      {/* Header */}
      <header className="w-full px-6 py-4 flex items-center justify-between bg-white/70 backdrop-blur-md border-b border-amber-100 sticky top-0 z-10">
        <div className="flex items-center gap-2">
          <div className="w-10 h-10 bg-amber-600 rounded-xl flex items-center justify-center">
            <Sparkles className="w-6 h-6 text-white" />
          </div>
          <h1 className="text-2xl font-bold text-amber-900">AntarAalay.ai</h1>
        </div>
        <div className="flex items-center gap-4">
          {user?.photoURL && (
            <img src={user.photoURL} alt="Profile" className="w-10 h-10 rounded-full" />
          )}
          <span className="text-amber-800 hidden sm:block">{user?.displayName || user?.email}</span>
          <button
            onClick={handleLogout}
            className="p-2 text-amber-700 hover:text-amber-900 hover:bg-amber-100 rounded-lg transition-all"
            title="Logout"
          >
            <LogOut className="w-5 h-5" />
          </button>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-6 py-8">
        {/* Welcome */}
        <div className="mb-10">
          <h2 className="text-3xl font-bold text-amber-950 mb-2">
            Welcome back, {user?.displayName?.split(' ')[0] || 'Designer'}!
          </h2>
          <p className="text-amber-700">Ready to create beautiful, Vastu-aligned spaces?</p>
        </div>

        {/* Quick Actions */}
        <div className="grid md:grid-cols-3 gap-6 mb-12">
          <Link
            to="/upload"
            className="group p-6 bg-white/80 backdrop-blur-sm rounded-2xl border border-amber-100 shadow-sm hover:shadow-lg transition-all"
          >
            <div className="w-14 h-14 bg-amber-100 rounded-xl flex items-center justify-center mb-4 group-hover:bg-amber-200 transition-all">
              <Plus className="w-7 h-7 text-amber-600" />
            </div>
            <h3 className="text-xl font-semibold text-amber-950 mb-2">Upload Room</h3>
            <p className="text-amber-700 mb-4">Add a new room and generate AI designs</p>
            <div className="flex items-center text-amber-600 font-medium">
              Get Started <ChevronRight className="w-4 h-4 ml-1" />
            </div>
          </Link>

          <Link
            to="/vastu"
            className="group p-6 bg-white/80 backdrop-blur-sm rounded-2xl border border-amber-100 shadow-sm hover:shadow-lg transition-all"
          >
            <div className="w-14 h-14 bg-orange-100 rounded-xl flex items-center justify-center mb-4 group-hover:bg-orange-200 transition-all">
              <Sparkles className="w-7 h-7 text-orange-600" />
            </div>
            <h3 className="text-xl font-semibold text-amber-950 mb-2">Vastu Analysis</h3>
            <p className="text-amber-700 mb-4">Check Vastu compliance for any room</p>
            <div className="flex items-center text-orange-600 font-medium">
              Analyze Now <ChevronRight className="w-4 h-4 ml-1" />
            </div>
          </Link>

          <div className="p-6 bg-gradient-to-br from-amber-600 to-orange-600 rounded-2xl text-white">
            <h3 className="text-xl font-semibold mb-2">Pro Tip</h3>
            <p className="text-amber-100 mb-4">
              Northeast is the best direction for prayer rooms and study areas according to Vastu.
            </p>
            <div className="text-sm text-amber-200">💡 Ancient Wisdom</div>
          </div>
        </div>

        {/* Recent Rooms */}
        <div>
          <div className="flex items-center justify-between mb-6">
            <h3 className="text-2xl font-bold text-amber-950">Your Rooms</h3>
            <Link to="/upload" className="text-amber-600 hover:text-amber-700 font-medium">
              + Add New
            </Link>
          </div>

          {isLoading ? (
            <div className="grid md:grid-cols-3 lg:grid-cols-4 gap-6">
              {[1, 2, 3, 4].map((i) => (
                <div key={i} className="aspect-square bg-amber-100/50 rounded-2xl animate-pulse" />
              ))}
            </div>
          ) : recentRooms.length === 0 ? (
            <div className="text-center py-16 bg-white/50 rounded-2xl border border-amber-100 border-dashed">
              <Image className="w-16 h-16 text-amber-300 mx-auto mb-4" />
              <h4 className="text-xl font-semibold text-amber-800 mb-2">No rooms yet</h4>
              <p className="text-amber-600 mb-6">Upload your first room to get started</p>
              <Link
                to="/upload"
                className="inline-block px-6 py-3 bg-amber-600 text-white rounded-xl font-medium hover:bg-amber-700 transition-all"
              >
                Upload Room
              </Link>
            </div>
          ) : (
            <div className="grid md:grid-cols-3 lg:grid-cols-4 gap-6">
              {recentRooms.map((room) => (
                <Link
                  key={room.room_id}
                  to={`/designs/${room.room_id}`}
                  className="group relative aspect-square bg-white/80 rounded-2xl overflow-hidden border border-amber-100 shadow-sm hover:shadow-lg transition-all"
                >
                  <img
                    src={room.images?.north}
                    alt="Room"
                    className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
                  />
                  <div className="absolute inset-0 bg-gradient-to-t from-amber-950/80 via-transparent to-transparent opacity-0 group-hover:opacity-100 transition-all">
                    <div className="absolute bottom-4 left-4 right-4">
                      <p className="text-white font-semibold capitalize">{room.room_type || 'Room'}</p>
                      <p className="text-amber-200 text-sm capitalize">{room.direction || 'Unknown direction'}</p>
                    </div>
                  </div>
                </Link>
              ))}
            </div>
          )}
        </div>
      </main>
    </div>
  );
}
