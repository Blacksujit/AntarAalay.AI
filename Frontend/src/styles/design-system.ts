/**
 * Vastu × AI Design System
 * AntarAalay.ai - Spatial Intelligence Platform
 * Ancient Wisdom + Modern Intelligence
 */

export const vastuAIDesignSystem = {
  // Core Philosophy Colors
  colors: {
    // Primary Palette - Architectural Harmony
    primary: {
      stone: '#F4EFE6',        // Warm stone foundation
      charcoal: '#1F1F1F',     // Deep architectural charcoal
      accentGold: '#C6A75E',   // Refined gold accent
      deepEarth: '#5C4B3C',    // Earth connection
      softSand: '#E8DFC8',     // Gentle sand
      white: '#FFFFFF',        // Pure light
    },
    
    // Directional Colors - Subtle Compass References
    directional: {
      north: '#E8F4FD',        // Cool, clear
      south: '#FFF4E6',        // Warm, bright
      east: '#F0FDF4',         // Fresh, new
      west: '#FEF3C7',         // Reflective, golden
    },
    
    // Semantic Colors
    semantic: {
      success: '#10B981',      // Harmony achieved
      warning: '#F59E0B',      // Attention needed
      error: '#EF4444',        // Imbalance
      info: '#3B82F6',         // Guidance
    },
  },
  
  // Typography - Ancient Wisdom Meets Modern Clarity
  typography: {
    fontFamily: {
      serif: ['Playfair Display', 'Cormorant Garamond', 'Georgia', 'serif'],
      sans: ['Inter', '-apple-system', 'BlinkMacSystemFont', 'sans-serif'],
      mono: ['JetBrains Mono', 'Fira Code', 'monospace'],
    },
    
    fontSize: {
      xs: '0.75rem',      // 12px
      sm: '0.875rem',     // 14px
      base: '1rem',       // 16px
      lg: '1.125rem',     // 18px
      xl: '1.25rem',      // 20px
      '2xl': '1.5rem',    // 24px
      '3xl': '1.875rem',  // 30px
      '4xl': '2.25rem',   // 36px
      '5xl': '3rem',      // 48px
      '6xl': '3.75rem',   // 60px
      '7xl': '4.5rem',    // 72px
      '8xl': '6rem',      // 96px
    },
    
    fontWeight: {
      light: 300,
      normal: 400,
      medium: 500,
      semibold: 600,
      bold: 700,
      extrabold: 800,
    },
  },
  
  // Motion System - Intentional Movement
  motion: {
    duration: {
      fast: '150ms',
      normal: '300ms',
      slow: '500ms',
      slower: '800ms',
      cinematic: '1200ms',
    },
    
    ease: {
      default: 'cubic-bezier(0.4, 0, 0.2, 1)',
      in: 'cubic-bezier(0.4, 0, 1, 1)',
      out: 'cubic-bezier(0, 0, 0.2, 1)',
      bounce: 'cubic-bezier(0.68, -0.55, 0.265, 1.55)',
      smooth: 'cubic-bezier(0.25, 0.46, 0.45, 0.94)',
      architectural: 'cubic-bezier(0.16, 1, 0.3, 1)',
    },
  },
  
  // Vastu-Specific Tokens
  vastu: {
    // Directional meanings
    directions: {
      north: { element: 'water', quality: 'prosperity', color: '#E8F4FD' },
      south: { element: 'fire', quality: 'reputation', color: '#FFF4E6' },
      east: { element: 'air', quality: 'health', color: '#F0FDF4' },
      west: { element: 'earth', quality: 'family', color: '#FEF3C7' },
    },
    
    // Compass animations
    compass: {
      rotateDuration: '20s',
      floatDuration: '3s',
      pulseDuration: '2s',
    },
  },
};

export default vastuAIDesignSystem;
