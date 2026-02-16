import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { useEffect } from 'react';
import { useAuthStore } from './store/authStore';
import { ErrorBoundary } from './components/ErrorBoundary';

// Pages
import Home from './pages/Home';
import Login from './pages/Login';
import Dashboard from './pages/Dashboard';
import Upload from './pages/Upload';
import Customize from './pages/Customize';
import Designs from './pages/Designs';
import Vastu from './pages/Vastu';

// Create Query Client
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 5 * 60 * 1000,
      retry: 1,
      refetchOnWindowFocus: false,
    },
  },
});

// Auth initializer component
function AuthInitializer({ children }: { children: React.ReactNode }) {
  const initializeAuth = useAuthStore((state) => state.initializeAuth);

  useEffect(() => {
    initializeAuth();
  }, []); // Empty dependency array - only run once on mount

  return <>{children}</>;
}

// Protected route component
function ProtectedRoute({ children }: { children: React.ReactNode }) {
  const { user, isLoading } = useAuthStore();

  if (isLoading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-amber-50 via-orange-50 to-rose-50 flex items-center justify-center">
        <div className="w-16 h-16 border-4 border-amber-200 border-t-amber-600 rounded-full animate-spin" />
      </div>
    );
  }

  if (!user) {
    return <Navigate to="/login" replace />;
  }

  return <>{children}</>;
}

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <AuthInitializer>
        <Router>
          <Routes>
            {/* Public routes */}
            <Route path="/" element={<ErrorBoundary><Home /></ErrorBoundary>} />
            <Route path="/login" element={<ErrorBoundary><Login /></ErrorBoundary>} />

            {/* Protected routes */}
            <Route
              path="/dashboard"
              element={
                <ProtectedRoute>
                  <ErrorBoundary><Dashboard /></ErrorBoundary>
                </ProtectedRoute>
              }
            />
            <Route
              path="/upload"
              element={
                <ProtectedRoute>
                  <ErrorBoundary><Upload /></ErrorBoundary>
                </ProtectedRoute>
              }
            />
            <Route
              path="/customize/:roomId"
              element={
                <ProtectedRoute>
                  <ErrorBoundary><Customize /></ErrorBoundary>
                </ProtectedRoute>
              }
            />
            <Route
              path="/designs/:roomId"
              element={
                <ProtectedRoute>
                  <ErrorBoundary><Designs /></ErrorBoundary>
                </ProtectedRoute>
              }
            />
            <Route
              path="/vastu"
              element={
                <ProtectedRoute>
                  <ErrorBoundary><Vastu /></ErrorBoundary>
                </ProtectedRoute>
              }
            />

            {/* Fallback */}
            <Route path="*" element={<Navigate to="/" replace />} />
          </Routes>
        </Router>
      </AuthInitializer>
    </QueryClientProvider>
  );
}

export default App;
