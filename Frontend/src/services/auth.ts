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

// Firebase configuration
const firebaseConfig = {
  apiKey: import.meta.env.VITE_FIREBASE_API_KEY || "AIzaSyANQciKqx_Cyi92ahSVaLy_MewUDkZY3fg",
  authDomain: import.meta.env.VITE_FIREBASE_AUTH_DOMAIN || "antaraalayai.firebaseapp.com",
  projectId: import.meta.env.VITE_FIREBASE_PROJECT_ID || "antaraalayai",
  storageBucket: import.meta.env.VITE_FIREBASE_STORAGE_BUCKET || "antaraalayai.firebasestorage.app",
  messagingSenderId: import.meta.env.VITE_FIREBASE_MESSAGING_SENDER_ID || "656663048044",
  appId: import.meta.env.VITE_FIREBASE_APP_ID || "1:656663048044:web:802e1ef31aaf30eb2a0d49",
  measurementId: import.meta.env.VITE_FIREBASE_MEASUREMENT_ID || "G-07QNHQGWJ0"
};

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
      localStorage.setItem('auth_token', token);
      
      return this.currentUser;
    } catch (error) {
      logger.error('Google sign-in error', { error }, error as Error);
      throw new Error('Failed to sign in with Google');
    }
  }

  async signOut(): Promise<void> {
    try {
      await signOut(auth);
      this.currentUser = null;
      localStorage.removeItem('auth_token');
    } catch (error) {
      logger.error('Sign out error', { error }, error as Error);
      throw new Error('Failed to sign out');
    }
  }

  getCurrentUser(): AuthUser | null {
    return this.currentUser;
  }

  onAuthStateChange(callback: (user: AuthUser | null) => void): () => void {
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
        localStorage.setItem('auth_token', token);
        callback(this.currentUser);
      } else {
        this.currentUser = null;
        localStorage.removeItem('auth_token');
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
