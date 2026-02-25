/**
 * Enterprise Main App
 * AntarAalay.ai - Luxury Interior Design Platform
 */

import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { useEffect } from 'react';
import { useAuthStore } from './store/authStore';
import { AppRouter } from './app/router';

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
  }, []);

  return <>{children}</>;
}

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <AuthInitializer>
        <div className="min-h-screen bg-brand-beige">
          <AppRouter />
        </div>
      </AuthInitializer>
    </QueryClientProvider>
  );
}

export default App;
