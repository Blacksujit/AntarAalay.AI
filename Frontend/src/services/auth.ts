/**
 * Module: Frontend Auth Service
 * 
 * Handles Firebase authentication with Google Sign-In.
 */
import { initializeApp, getApps } from 'firebase/app';
import type { FirebaseApp } from 'firebase/app';
import type { User } from 'firebase/auth';
import {
  getAuth,
  GoogleAuthProvider,
  signInWithPopup,
  signOut,
  onAuthStateChanged,
} from 'firebase/auth';
import { logger } from '../utils/logger';

function getRequiredEnv(name: string): string {
  const value = process.env[name];
  if (!value) {
    throw new Error(
      `Missing required environment variable: ${name}. ` +
        `Create/Update Frontend/.env.local (or .env) and restart the Next.js dev server.`
    );
  }
  return value;
}

// Firebase configuration
const firebaseConfig = {
  apiKey: process.env.NEXT_PUBLIC_FIREBASE_API_KEY || "",
  authDomain: process.env.NEXT_PUBLIC_FIREBASE_AUTH_DOMAIN || "",
  projectId: process.env.NEXT_PUBLIC_FIREBASE_PROJECT_ID || "",
  storageBucket: process.env.NEXT_PUBLIC_FIREBASE_STORAGE_BUCKET || "",
  messagingSenderId: process.env.NEXT_PUBLIC_FIREBASE_MESSAGING_SENDER_ID || "",
  appId: process.env.NEXT_PUBLIC_FIREBASE_APP_ID || "",
  measurementId: process.env.NEXT_PUBLIC_FIREBASE_MEASUREMENT_ID || "",
};

const isBrowser = typeof window !== 'undefined';

// Initialize Firebase (singleton)
let app: FirebaseApp;
if (getApps().length === 0) {
  app = initializeApp(firebaseConfig);
} else {
  app = getApps()[0];
}

const auth = getAuth(app);
const googleProvider = new GoogleAuthProvider();

export interface AuthUser {
  uid: string;
  email: string | null;
  displayName: string | null;
  photoURL: string | null;
  token: string | null;
}

class AuthService {
  private currentUser: AuthUser | null = null;

  async signInWithGoogle(): Promise<AuthUser | null> {
    if (!isBrowser) {
      throw new Error('Google sign-in is only available in the browser');
    }
    try {
      const result = await signInWithPopup(auth, googleProvider);
      const user = result.user;
      const token = await user.getIdToken();
      
      this.currentUser = {
        uid: user.uid,
        email: user.email,
        displayName: user.displayName,
        photoURL: user.photoURL,
        token: token
      };
      
      // Store token for API calls
      window.localStorage.setItem('auth_token', token);
      
      return this.currentUser;
    } catch (error) {
      logger.error('Google sign-in error', { error }, error as Error);
      throw new Error('Failed to sign in with Google');
    }
  }

  async signOut(): Promise<void> {
    if (!isBrowser) return;
    try {
      await signOut(auth);
      this.currentUser = null;
      window.localStorage.removeItem('auth_token');
    } catch (error) {
      logger.error('Sign out error', { error }, error as Error);
      throw new Error('Failed to sign out');
    }
  }

  getCurrentUser(): AuthUser | null {
    return this.currentUser;
  }

  onAuthStateChange(callback: (user: AuthUser | null) => void): () => void {
    if (!isBrowser) {
      return () => undefined;
    }
    return onAuthStateChanged(auth, async (firebaseUser: User | null) => {
      if (firebaseUser) {
        const token = await firebaseUser.getIdToken();
        this.currentUser = {
          uid: firebaseUser.uid,
          email: firebaseUser.email,
          displayName: firebaseUser.displayName,
          photoURL: firebaseUser.photoURL,
          token: token
        };
        window.localStorage.setItem('auth_token', token);
        callback(this.currentUser);
      } else {
        this.currentUser = null;
        window.localStorage.removeItem('auth_token');
        callback(null);
      }
    });
  }

  async getToken(): Promise<string | null> {
    if (this.currentUser?.token) {
      return this.currentUser.token;
    }
    const user = auth.currentUser;
    if (user) {
      return await user.getIdToken();
    }
    return null;
  }
}

export const authService = new AuthService();
export { auth, googleProvider };

// Helpers for Zustand authStore (keeps existing behavior)
export async function signInWithGoogle(): Promise<{ user: User; token: string }> {
  const result = await signInWithPopup(auth, googleProvider);
  const token = await result.user.getIdToken();
  if (typeof window !== 'undefined') {
    window.localStorage.setItem('auth_token', token);
  }
  return { user: result.user, token };
}

export async function logoutUser(): Promise<void> {
  await authService.signOut();
}

export async function getCurrentUser(): Promise<User | null> {
  if (typeof window === 'undefined') return null;
  return auth.currentUser;
}

export async function getIdToken(user: User, forceRefresh?: boolean): Promise<string> {
  return user.getIdToken(forceRefresh);
}
