import { create } from 'zustand';
import { persist, createJSONStorage } from 'zustand/middleware';
import type { User } from 'firebase/auth';
import { 
  signInWithGoogle, 
  logoutUser, 
  getCurrentUser, 
  getIdToken 
} from '../lib/firebase';

interface AuthState {
  user: User | null;
  token: string | null;
  isLoading: boolean;
  error: string | null;
  
  // Actions
  setUser: (user: User | null) => void;
  setToken: (token: string | null) => void;
  setLoading: (loading: boolean) => void;
  setError: (error: string | null) => void;
  
  signIn: () => Promise<void>;
  logout: () => Promise<void>;
  initializeAuth: () => Promise<void>;
  refreshToken: () => Promise<string | null>;
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set, get) => ({
      user: null,
      token: null,
      isLoading: false,
      error: null,

      setUser: (user) => set({ user }),
      setToken: (token) => {
        set({ token });
        if (token) {
          localStorage.setItem('auth_token', token);
        } else {
          localStorage.removeItem('auth_token');
        }
      },
      setLoading: (isLoading) => set({ isLoading }),
      setError: (error) => set({ error }),

      signIn: async () => {
        set({ isLoading: true, error: null });
        try {
          const { user, token } = await signInWithGoogle();
          set({ user, token, isLoading: false });
          localStorage.setItem('auth_token', token);
        } catch (error) {
          set({ 
            error: error instanceof Error ? error.message : 'Sign in failed', 
            isLoading: false 
          });
          throw error;
        }
      },

      logout: async () => {
        set({ isLoading: true });
        try {
          await logoutUser();
          set({ user: null, token: null, isLoading: false, error: null });
          localStorage.removeItem('auth_token');
        } catch (error) {
          set({ 
            error: error instanceof Error ? error.message : 'Logout failed', 
            isLoading: false 
          });
          throw error;
        }
      },

      initializeAuth: async () => {
        set({ isLoading: true });
        try {
          const user = await getCurrentUser();
          if (user) {
            const token = await getIdToken(user);
            set({ user, token, isLoading: false });
            localStorage.setItem('auth_token', token);
          } else {
            set({ isLoading: false });
          }
        } catch (error) {
          set({ 
            error: error instanceof Error ? error.message : 'Auth initialization failed', 
            isLoading: false 
          });
        }
      },

      refreshToken: async () => {
        const { user } = get();
        if (user) {
          try {
            const token = await getIdToken(user, true);
            set({ token });
            localStorage.setItem('auth_token', token);
            return token;
          } catch (error) {
            console.error('Token refresh failed:', error);
            return null;
          }
        }
        return null;
      },
    }),
    {
      name: 'auth-storage',
      storage: createJSONStorage(() => localStorage),
      partialize: (state) => ({ user: state.user, token: state.token }),
      skipHydration: true,
    }
  )
);
