/**
 * Enterprise Global State Management
 * AntarAalay.ai - Luxury Interior Design Platform
 */

import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import type { User } from 'firebase/auth';

// Types
export interface Room {
  id: string;
  user_id: string;
  image_url: string;
  room_type: string;
  direction: string;
  created_at: string;
}

export interface Design {
  id: string;
  room_id: string;
  user_id: string;
  style: string;
  budget?: number;
  wall_color?: string;
  flooring_material?: string;
  image_1_url?: string;
  image_2_url?: string;
  image_3_url?: string;
  estimated_cost?: number;
  budget_match_percentage?: number;
  vastu_score?: number;
  vastu_suggestions?: string[];
  vastu_warnings?: string[];
  status: string;
  created_at: string;
}

export interface DesignCustomization {
  style: string;
  wall_color: string;
  flooring_material: string;
  budget?: number;
}

export type GenerationStatus = 
  | 'idle' 
  | 'uploading' 
  | 'generating' 
  | 'completed' 
  | 'error';

export interface GenerationProgress {
  status: GenerationStatus;
  progress: number;
  message: string;
  estimatedTimeRemaining?: number;
}

export interface UsageStats {
  dailyGenerations: number;
  dailyLimit: number;
  monthlyGenerations: number;
  lastResetDate: string;
}

// Global State Interface
interface GlobalState {
  // User & Authentication
  user: User | null;
  isAuthenticated: boolean;
  
  // Current Room Context
  currentRoom: Room | null;
  uploadedImages: Record<string, File | null>;
  roomId: string | null;
  
  // Design Generation State
  generationProgress: GenerationProgress;
  currentDesigns: Design[];
  selectedCustomization: DesignCustomization;
  
  // Usage Tracking
  usageStats: UsageStats;
  
  // UI State
  sidebarOpen: boolean;
  activeModal: string | null;
  toastMessage: string | null;
  
  // Actions
  setUser: (user: User | null) => void;
  setCurrentRoom: (room: Room | null) => void;
  setUploadedImages: (images: Record<string, File | null>) => void;
  setRoomId: (roomId: string | null) => void;
  
  // Generation Actions
  startGeneration: () => void;
  updateGenerationProgress: (progress: Partial<GenerationProgress>) => void;
  completeGeneration: (designs: Design[]) => void;
  failGeneration: (error: string) => void;
  resetGeneration: () => void;
  
  // Customization Actions
  setSelectedCustomization: (customization: Partial<DesignCustomization>) => void;
  
  // Usage Actions
  incrementUsage: () => void;
  resetDailyUsage: () => void;
  setUsageStats: (stats: Partial<UsageStats>) => void;
  
  // UI Actions
  toggleSidebar: () => void;
  openModal: (modalId: string) => void;
  closeModal: () => void;
  showToast: (message: string) => void;
  clearToast: () => void;
  
  // Clear all state (logout)
  clearState: () => void;
}

// Default customization values
const defaultCustomization: DesignCustomization = {
  style: 'modern',
  wall_color: 'white',
  flooring_material: 'hardwood',
};

// Create the store with persistence
export const useGlobalStore = create<GlobalState>()(
  persist(
    (set, get) => ({
      // Initial State
      user: null,
      isAuthenticated: false,
      
      currentRoom: null,
      uploadedImages: { north: null, south: null, east: null, west: null },
      roomId: null,
      
      generationProgress: {
        status: 'idle',
        progress: 0,
        message: '',
      },
      currentDesigns: [],
      selectedCustomization: defaultCustomization,
      
      usageStats: {
        dailyGenerations: 0,
        dailyLimit: 3,
        monthlyGenerations: 0,
        lastResetDate: new Date().toISOString(),
      },
      
      sidebarOpen: true,
      activeModal: null,
      toastMessage: null,
      
      // User Actions
      setUser: (user) => set({ 
        user, 
        isAuthenticated: !!user 
      }),
      
      // Room Actions
      setCurrentRoom: (room) => set({ currentRoom: room }),
      setUploadedImages: (images) => set({ uploadedImages: images }),
      setRoomId: (roomId) => set({ roomId }),
      
      // Generation Actions
      startGeneration: () => set({
        generationProgress: {
          status: 'generating',
          progress: 0,
          message: 'Initializing AI design generation...',
          estimatedTimeRemaining: 60,
        },
        currentDesigns: [],
      }),
      
      updateGenerationProgress: (progress) => set((state) => ({
        generationProgress: {
          ...state.generationProgress,
          ...progress,
        },
      })),
      
      completeGeneration: (designs) => set({
        generationProgress: {
          status: 'completed',
          progress: 100,
          message: 'Design generation complete!',
        },
        currentDesigns: designs,
      }),
      
      failGeneration: (error) => set({
        generationProgress: {
          status: 'error',
          progress: 0,
          message: error,
        },
      }),
      
      resetGeneration: () => set({
        generationProgress: {
          status: 'idle',
          progress: 0,
          message: '',
        },
        currentDesigns: [],
      }),
      
      // Customization Actions
      setSelectedCustomization: (customization) => set((state) => ({
        selectedCustomization: {
          ...state.selectedCustomization,
          ...customization,
        },
      })),
      
      // Usage Actions
      incrementUsage: () => set((state) => ({
        usageStats: {
          ...state.usageStats,
          dailyGenerations: state.usageStats.dailyGenerations + 1,
          monthlyGenerations: state.usageStats.monthlyGenerations + 1,
        },
      })),
      
      resetDailyUsage: () => set((state) => ({
        usageStats: {
          ...state.usageStats,
          dailyGenerations: 0,
          lastResetDate: new Date().toISOString(),
        },
      })),
      
      setUsageStats: (stats) => set((state) => ({
        usageStats: {
          ...state.usageStats,
          ...stats,
        },
      })),
      
      // UI Actions
      toggleSidebar: () => set((state) => ({ 
        sidebarOpen: !state.sidebarOpen 
      })),
      
      openModal: (modalId) => set({ activeModal: modalId }),
      closeModal: () => set({ activeModal: null }),
      
      showToast: (message) => set({ toastMessage: message }),
      clearToast: () => set({ toastMessage: null }),
      
      // Clear State (Logout)
      clearState: () => set({
        user: null,
        isAuthenticated: false,
        currentRoom: null,
        uploadedImages: { north: null, south: null, east: null, west: null },
        roomId: null,
        generationProgress: {
          status: 'idle',
          progress: 0,
          message: '',
        },
        currentDesigns: [],
        selectedCustomization: defaultCustomization,
      }),
    }),
    {
      name: 'antaraalay-global-storage',
      partialize: (state) => ({
        // Only persist these fields
        usageStats: state.usageStats,
        selectedCustomization: state.selectedCustomization,
      }),
    }
  )
);

// Selectors for computed values
export const selectCanGenerate = (state: GlobalState): boolean => {
  return state.usageStats.dailyGenerations < state.usageStats.dailyLimit;
};

export const selectRemainingGenerations = (state: GlobalState): number => {
  return Math.max(0, state.usageStats.dailyLimit - state.usageStats.dailyGenerations);
};

export const selectIsGenerating = (state: GlobalState): boolean => {
  return state.generationProgress.status === 'generating';
};

export const selectAllImagesUploaded = (state: GlobalState): boolean => {
  const images = state.uploadedImages;
  return !!images.north && !!images.south && !!images.east && !!images.west;
};
