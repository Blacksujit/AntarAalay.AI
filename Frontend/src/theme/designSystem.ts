/**
 * Premium Interior Design System
 * AntarAalay.ai - Architectural Design Tokens
 */

export const designTokens = {
  // Colors - Interior Inspired Palette
  colors: {
    // Primary Colors
    primary: {
      background: '#F4EFE6', // Warm stone
      surface: '#FFFFFF', // Soft highlight
      charcoal: '#1E1E1E', // Architectural charcoal
      gold: '#BFA46F', // Muted gold
      grey: '#DADADA', // Neutral grey
    },
    
    // Semantic Colors
    semantic: {
      success: '#10B981',
      warning: '#F59E0B',
      error: '#EF4444',
      info: '#3B82F6',
    },
    
    // Surface Colors
    surface: {
      elevated: '#FFFFFF',
      overlay: 'rgba(30, 30, 30, 0.8)',
      glass: 'rgba(255, 255, 255, 0.7)',
      card: '#FFFFFF',
    },
    
    // Text Colors
    text: {
      primary: '#1E1E1E',
      secondary: '#666666',
      tertiary: '#999999',
      inverse: '#FFFFFF',
    },
  },
  
  // Typography - Luxury Scale
  typography: {
    fontFamily: {
      serif: ['Playfair Display', 'Cormorant Garamond', 'Georgia', 'serif'],
      sans: ['Inter', '-apple-system', 'BlinkMacSystemFont', 'sans-serif'],
      mono: ['JetBrains Mono', 'Fira Code', 'monospace'],
    },
    
    fontSize: {
      xs: '0.75rem',    // 12px
      sm: '0.875rem',   // 14px
      base: '1rem',     // 16px
      lg: '1.125rem',   // 18px
      xl: '1.25rem',    // 20px
      '2xl': '1.5rem',  // 24px
      '3xl': '1.875rem', // 30px
      '4xl': '2.25rem', // 36px
      '5xl': '3rem',    // 48px
      '6xl': '3.75rem', // 60px
      '7xl': '4.5rem',  // 72px
      '8xl': '6rem',    // 96px
    },
    
    fontWeight: {
      light: 300,
      normal: 400,
      medium: 500,
      semibold: 600,
      bold: 700,
      extrabold: 800,
    },
    
    lineHeight: {
      tight: 1.25,
      normal: 1.5,
      relaxed: 1.75,
    },
    
    letterSpacing: {
      tight: '-0.025em',
      normal: '0',
      wide: '0.025em',
      wider: '0.05em',
      widest: '0.1em',
    },
  },
  
  // Motion System
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
    },
    
    scale: {
      subtle: '1.02',
      medium: '1.05',
      large: '1.1',
    },
    
    opacity: {
      hidden: 0,
      subtle: 0.7,
      visible: 1,
    },
  },
};

export default designTokens;
