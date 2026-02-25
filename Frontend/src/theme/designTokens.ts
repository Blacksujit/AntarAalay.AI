/**
 * Premium Interior Design Theme
 * AntarAalay.ai - Luxury Design System
 */

export const designTokens = {
  // Colors - Interior Design Palette
  colors: {
    // Primary - Warm Neutrals
    primary: {
      50: '#FEFAF6',
      100: '#F5F1E8', // Warm beige background
      200: '#E8E0D0',
      300: '#D4C5B0',
      400: '#C6A75E', // Gold accent
      500: '#B8941F',
      600: '#9A7A1A',
      700: '#7C6215',
      800: '#5E4B0F',
      900: '#2A2A2A', // Charcoal
    },
    
    // Secondary - Soft Grays
    secondary: {
      50: '#F9FAFB',
      100: '#F3F4F6',
      200: '#E5E7EB',
      300: '#D1D5DB',
      400: '#9CA3AF',
      500: '#6B7280',
      600: '#4B5563',
      700: '#374151',
      800: '#1F2937',
      900: '#111827',
    },
    
    // Accent - Interior Colors
    accent: {
      teal: '#14B8A6',
      sage: '#84CC16',
      terracotta: '#F97316',
      blush: '#EC4899',
      navy: '#1E40AF',
    },
    
    // Semantic
    semantic: {
      success: '#10B981',
      warning: '#F59E0B',
      error: '#EF4444',
      info: '#3B82F6',
    },
    
    // Glass Effects
    glass: {
      light: 'rgba(245, 241, 232, 0.8)',
      medium: 'rgba(245, 241, 232, 0.6)',
      dark: 'rgba(42, 42, 42, 0.8)',
    },
  },
  
  // Typography - Luxury Fonts
  typography: {
    fontFamily: {
      serif: "'Playfair Display', Georgia, serif", // Luxury headings
      sans: "'Inter', -apple-system, BlinkMacSystemFont, sans-serif", // Clean body
      mono: "'JetBrains Mono', 'Fira Code', monospace", // Code
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
  },
  
  // Spacing - 8px Grid System
  spacing: {
    0: '0',
    1: '0.25rem',   // 4px
    2: '0.5rem',    // 8px
    3: '0.75rem',   // 12px
    4: '1rem',      // 16px
    5: '1.25rem',   // 20px
    6: '1.5rem',    // 24px
    8: '2rem',      // 32px
    10: '2.5rem',   // 40px
    12: '3rem',     // 48px
    16: '4rem',     // 64px
    20: '5rem',     // 80px
    24: '6rem',     // 96px
    32: '8rem',     // 128px
  },
  
  // Shadows - Luxury Effects
  shadows: {
    soft: '0 2px 15px -3px rgba(0, 0, 0, 0.07), 0 10px 20px -2px rgba(0, 0, 0, 0.04)',
    medium: '0 4px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04)',
    luxury: '0 20px 40px -12px rgba(0, 0, 0, 0.15), 0 8px 16px -8px rgba(0, 0, 0, 0.1)',
    glow: '0 0 20px rgba(198, 167, 94, 0.3)',
    inner: 'inset 0 2px 4px 0 rgba(0, 0, 0, 0.06)',
  },
  
  // Border Radius
  borderRadius: {
    none: '0',
    sm: '0.125rem',   // 2px
    base: '0.25rem',  // 4px
    md: '0.375rem',   // 6px
    lg: '0.5rem',     // 8px
    xl: '0.75rem',    // 12px
    '2xl': '1rem',    // 16px
    '3xl': '1.5rem',  // 24px
    full: '9999px',
  },
  
  // Animation
  animation: {
    duration: {
      fast: '150ms',
      normal: '300ms',
      slow: '500ms',
      slower: '800ms',
    },
    
    ease: {
      default: 'cubic-bezier(0.4, 0, 0.2, 1)',
      in: 'cubic-bezier(0.4, 0, 1, 1)',
      out: 'cubic-bezier(0, 0, 0.2, 1)',
      bounce: 'cubic-bezier(0.68, -0.55, 0.265, 1.55)',
    },
  },
  
  // Breakpoints
  breakpoints: {
    sm: '640px',
    md: '768px',
    lg: '1024px',
    xl: '1280px',
    '2xl': '1536px',
  },
  
  // Z-Index
  zIndex: {
    dropdown: 1000,
    sticky: 1020,
    fixed: 1030,
    modalBackdrop: 1040,
    modal: 1050,
    popover: 1060,
    tooltip: 1070,
    toast: 1080,
  },
};

// CSS Custom Properties for runtime theming
export const cssVariables = {
  '--color-primary-50': designTokens.colors.primary[50],
  '--color-primary-100': designTokens.colors.primary[100],
  '--color-primary-400': designTokens.colors.primary[400],
  '--color-primary-900': designTokens.colors.primary[900],
  '--color-glass-light': designTokens.colors.glass.light,
  '--color-glass-dark': designTokens.colors.glass.dark,
  '--font-serif': designTokens.typography.fontFamily.serif,
  '--font-sans': designTokens.typography.fontFamily.sans,
  '--shadow-luxury': designTokens.shadows.luxury,
  '--shadow-glow': designTokens.shadows.glow,
};

export default designTokens;
