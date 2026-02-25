/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      // Luxury color palette
      colors: {
        // Brand colors
        'brand': {
          'beige': '#F5F1E8',
          'charcoal': '#2A2A2A',
          'gold': '#C6A75E',
          'white': '#FAFAFA',
        },
        
        // Extended palette
        'warm': {
          '50': '#FEF9F5',
          '100': '#FDF3E7',
          '200': '#F8EAD7',
          '300': '#F3DDD0',
          '400': '#EED0C9',
          '500': '#E8C3BC',
          '600': '#D4A373',
          '700': '#BF8349',
          '800': '#9C6E3A',
          '900': '#785A2C',
        },
        
        'neutral': {
          '50': '#FAFAFA',
          '100': '#F5F5F5',
          '200': '#E5E5E5',
          '300': '#D4D4D4',
          '400': '#A3A3A3',
          '500': '#737373',
          '600': '#525252',
          '700': '#404040',
          '800': '#262626',
          '900': '#171717',
        },
        
        'gold': {
          '50': '#FFFBF0',
          '100': '#FEF3C7',
          '200': '#FDE68A',
          '300': '#FCD34D',
          '400': '#FBBF24',
          '500': '#F59E0B',
          '600': '#D97706',
          '700': '#B45309',
          '800': '#92400E',
          '900': '#78350F',
        }
      },
      
      // Luxury typography
      fontFamily: {
        'display': ['Playfair Display', 'Georgia', 'serif'],
        'body': ['Inter', 'system-ui', 'sans-serif'],
        'mono': ['JetBrains Mono', 'monospace'],
      },
      
      // Premium spacing system
      spacing: {
        '18': '4.5rem',
        '88': '22rem',
        '112': '28rem',
        '128': '32rem',
        '144': '36rem',
      },
      
      // Luxury shadows
      boxShadow: {
        'luxury': '0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04)',
        'soft': '0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)',
        'glow': '0 0 20px rgba(198, 167, 94, 0.3)',
        'glass': '0 8px 32px 0 rgba(31, 38, 135, 0.37)',
      },
      
      // Smooth animations
      animation: {
        'fade-in': 'fadeIn 0.6s ease-out',
        'slide-up': 'slideUp 0.5s ease-out',
        'shimmer': 'shimmer 2s linear infinite',
        'float': 'float 6s ease-in-out infinite',
      },
      
      keyframes: {
        fadeIn: {
          '0%': { opacity: '0' },
          '100%': { opacity: '1' },
        },
        slideUp: {
          '0%': { transform: 'translateY(20px)', opacity: '0' },
          '100%': { transform: 'translateY(0)', opacity: '1' },
        },
        shimmer: {
          '0%': { backgroundPosition: '-1000px 0' },
          '100%': { backgroundPosition: '1000px 0' },
        },
        float: {
          '0%, 100%': { transform: 'translateY(0px)' },
          '50%': { transform: 'translateY(-10px)' },
        },
      },
      
      // Glassmorphism
      backdropBlur: {
        'glass': '12px',
      },
    },
  },
  plugins: [],
}

