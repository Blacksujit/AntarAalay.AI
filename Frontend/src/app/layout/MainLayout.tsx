/**
 * Enterprise Main Layout
 * Combines sidebar, topnav, and responsive content area
 */

import { Outlet } from 'react-router-dom';
import { motion } from 'framer-motion';
import { Sidebar } from './Sidebar';
import { TopNav } from './TopNav';
import { useGlobalStore } from '../../store/globalStore';
import { GenerationLoader } from '../../components/ui/Loading';

export const MainLayout = () => {
  const sidebarOpen = useGlobalStore((state) => state.sidebarOpen);
  const generationProgress = useGlobalStore((state) => state.generationProgress);

  return (
    <div className="min-h-screen bg-brand-beige">
      {/* Fixed Navigation */}
      <Sidebar />
      <TopNav />

      {/* Main Content Area */}
      <motion.main
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ duration: 0.5 }}
        className={`
          min-h-screen pt-16 transition-all duration-300
          ${sidebarOpen ? 'pl-72' : 'pl-0'}
        `}
      >
        <div className="p-6 max-w-[1440px] mx-auto">
          <Outlet />
        </div>
      </motion.main>

      {/* Generation Loading Overlay */}
      <GenerationLoader
        isOpen={generationProgress.status === 'generating'}
        progress={generationProgress.progress}
        message={generationProgress.message}
        estimatedTime={generationProgress.estimatedTimeRemaining}
      />
    </div>
  );
};
