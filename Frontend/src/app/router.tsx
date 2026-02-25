/**
 * Enterprise React Router
 * Lazy-loaded routes for optimal performance
 */

import { Suspense, lazy } from 'react';
import { 
  createBrowserRouter, 
  RouterProvider, 
  Navigate,
  Outlet
} from 'react-router-dom';
import { motion } from 'framer-motion';
import { MainLayout } from './layout/MainLayout';
import { useAuthStore } from '../store/authStore';

// Loading fallback for lazy routes
const PageLoader = () => (
  <motion.div
    initial={{ opacity: 0 }}
    animate={{ opacity: 1 }}
    exit={{ opacity: 0 }}
    className="flex items-center justify-center min-h-screen"
  >
    <div className="flex flex-col items-center gap-4">
      <motion.div
        animate={{ rotate: 360 }}
        transition={{ duration: 1, repeat: Infinity, ease: 'linear' }}
        className="w-12 h-12 border-4 border-brand-gold/30 border-t-brand-gold rounded-full"
      />
      <p className="text-neutral-500 font-medium">Loading...</p>
    </div>
  </motion.div>
);

// Protected Route wrapper
const ProtectedRoute = () => {
  const { isAuthenticated, isLoading } = useAuthStore();
  
  if (isLoading) {
    return <PageLoader />;
  }
  
  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }
  
  return <Outlet />;
};

// Lazy load premium components
const Landing = lazy(() => import('../pages/LandingNew'));
const Login = lazy(() => import('../pages/Login'));
const OnboardingFlow = lazy(() => import('../features/onboarding/OnboardingFlow'));
const PremiumDashboard = lazy(() => import('../features/dashboard/PremiumDashboard'));
const PremiumUpload = lazy(() => import('../features/upload/PremiumUpload'));
const PremiumGeneration = lazy(() => import('../features/design/PremiumGeneration'));
const DesignView = lazy(() => import('./pages/PlaceholderPages').then(m => ({ default: m.DesignView })));
const History = lazy(() => import('./pages/PlaceholderPages').then(m => ({ default: m.History })));
const Profile = lazy(() => import('./pages/PlaceholderPages').then(m => ({ default: m.Profile })));
const Compare = lazy(() => import('./pages/PlaceholderPages').then(m => ({ default: m.Compare })));
const Vastu = lazy(() => import('./pages/PlaceholderPages').then(m => ({ default: m.Vastu })));
const NotFound = lazy(() => import('./pages/PlaceholderPages').then(m => ({ default: m.NotFound })));

// Create router
const router = createBrowserRouter([
  {
    path: '/',
    element: (
      <Suspense fallback={<PageLoader />}>
        <Landing />
      </Suspense>
    ),
  },
  {
    path: '/login',
    element: (
      <Suspense fallback={<PageLoader />}>
        <Login />
      </Suspense>
    ),
  },
  {
    path: '/',
    element: <ProtectedRoute />,
    children: [
      {
        path: '/',
        element: <MainLayout />,
        children: [
          {
            path: '/dashboard',
            element: (
              <Suspense fallback={<PageLoader />}>
                <PremiumDashboard />
              </Suspense>
            ),
          },
          {
            path: '/upload',
            element: (
              <Suspense fallback={<PageLoader />}>
                <PremiumUpload />
              </Suspense>
            ),
          },
          {
            path: '/design',
            element: (
              <Suspense fallback={<PageLoader />}>
                <PremiumGeneration />
              </Suspense>
            ),
          },
          {
            path: '/onboarding',
            element: (
              <Suspense fallback={<PageLoader />}>
                <OnboardingFlow />
              </Suspense>
            ),
          },
          {
            path: 'design/:id',
            element: (
              <Suspense fallback={<PageLoader />}>
                <DesignView />
              </Suspense>
            ),
          },
          {
            path: 'history',
            element: (
              <Suspense fallback={<PageLoader />}>
                <History />
              </Suspense>
            ),
          },
          {
            path: 'profile',
            element: (
              <Suspense fallback={<PageLoader />}>
                <Profile />
              </Suspense>
            ),
          },
          {
            path: 'compare',
            element: (
              <Suspense fallback={<PageLoader />}>
                <Compare />
              </Suspense>
            ),
          },
          {
            path: 'vastu',
            element: (
              <Suspense fallback={<PageLoader />}>
                <Vastu />
              </Suspense>
            ),
          },
        ],
      },
    ],
  },
  {
    path: '*',
    element: (
      <Suspense fallback={<PageLoader />}>
        <NotFound />
      </Suspense>
    ),
  },
]);

export const AppRouter = () => <RouterProvider router={router} />;
