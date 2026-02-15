import { vi } from 'vitest';
import '@testing-library/jest-dom';

// Mock Firebase
vi.mock('firebase/app', () => ({
  initializeApp: vi.fn(() => ({})),
  getApps: vi.fn(() => []),
}));

vi.mock('firebase/auth', () => ({
  getAuth: vi.fn(() => ({
    currentUser: null,
  })),
  GoogleAuthProvider: vi.fn(() => ({})),
  signInWithPopup: vi.fn(),
  signOut: vi.fn(),
  onAuthStateChanged: vi.fn(() => vi.fn()),
}));

// Mock environment variables
vi.mock('import.meta.env', () => ({
  VITE_FIREBASE_API_KEY: 'test-api-key',
  VITE_FIREBASE_PROJECT_ID: 'test-project',
  VITE_API_URL: 'http://localhost:8000',
}));
