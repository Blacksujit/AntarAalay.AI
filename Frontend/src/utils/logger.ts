/**
 * Logger utility for consistent error logging across the application
 * In development: logs to console
 * In production: could be extended to send to error tracking service (Sentry, LogRocket, etc.)
 */

import { clsx, type ClassValue } from 'clsx';
import { twMerge } from 'tailwind-merge';

type LogLevel = 'debug' | 'info' | 'warn' | 'error';

interface LogEntry {
  level: LogLevel;
  message: string;
  timestamp: string;
  context?: Record<string, unknown>;
  error?: Error;
}

/**
 * Merge Tailwind CSS classes with clsx
 */
export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

/**
 * Design tokens for luxury interior design
 */
export const design = {
  colors: {
    brand: {
      beige: '#F5F1E8',
      charcoal: '#2A2A2A',
      gold: '#C6A75E',
      white: '#FAFAFA',
    },
    warm: {
      50: '#FEF9F5',
      100: '#FDF3E7',
      200: '#F8EAD7',
      300: '#F3DDD0',
      400: '#EED0C9',
      500: '#E8C3BC',
      600: '#D4A373',
      700: '#BF8349',
      800: '#9C6E3A',
      900: '#785A2C',
    },
    neutral: {
      50: '#FAFAFA',
      100: '#F5F5F5',
      200: '#E5E5E5',
      300: '#D4D4D4',
      400: '#A3A3A3',
      500: '#737373',
      600: '#525252',
      700: '#404040',
      800: '#262626',
      900: '#171717',
    },
    gold: {
      50: '#FFFBF0',
      100: '#FEF3C7',
      200: '#FDE68A',
      300: '#FCD34D',
      400: '#FBBF24',
      500: '#F59E0B',
      600: '#D97706',
      700: '#B45309',
      800: '#92400E',
      900: '#78350F',
    },
  },
  
  typography: {
    fontFamily: {
      display: ['Playfair Display', 'Georgia', 'serif'],
      body: ['Inter', 'system-ui', 'sans-serif'],
      mono: ['JetBrains Mono', 'monospace'],
    },
  },
  
  shadows: {
    luxury: '0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04)',
    soft: '0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)',
    glow: '0 0 20px rgba(198, 167, 94, 0.3)',
    glass: '0 8px 32px 0 rgba(31, 38, 135, 0.37)',
  },
} as const;

export type Design = typeof design;

class Logger {
  private isDevelopment = process.env.NODE_ENV !== 'production';
  private logs: LogEntry[] = [];
  private maxLogs = 100;

  private createEntry(
    level: LogLevel,
    message: string,
    context?: Record<string, unknown>,
    error?: Error
  ): LogEntry {
    return {
      level,
      message,
      timestamp: new Date().toISOString(),
      context,
      error,
    };
  }

  private addToBuffer(entry: LogEntry) {
    this.logs.push(entry);
    if (this.logs.length > this.maxLogs) {
      this.logs.shift();
    }
  }

  private formatMessage(entry: LogEntry): string {
    const prefix = `[${entry.timestamp}] [${entry.level.toUpperCase()}]`;
    return `${prefix} ${entry.message}`;
  }

  debug(message: string, context?: Record<string, unknown>) {
    if (this.isDevelopment) {
      const entry = this.createEntry('debug', message, context);
      this.addToBuffer(entry);
      console.debug(this.formatMessage(entry), context || '');
    }
  }

  info(message: string, context?: Record<string, unknown>) {
    const entry = this.createEntry('info', message, context);
    this.addToBuffer(entry);
    console.info(this.formatMessage(entry), context || '');
  }

  warn(message: string, context?: Record<string, unknown>) {
    const entry = this.createEntry('warn', message, context);
    this.addToBuffer(entry);
    console.warn(this.formatMessage(entry), context || '');
  }

  error(message: string, context?: Record<string, unknown>, error?: Error) {
    const entry = this.createEntry('error', message, context, error);
    this.addToBuffer(entry);
    
    console.error(this.formatMessage(entry), context || '', error || '');
    
    // In production, you could send to error tracking service here
    if (!this.isDevelopment) {
      // Example: Sentry.captureException(error || new Error(message));
      this.sendToErrorTracking(entry);
    }
  }

  private sendToErrorTracking(_entry: LogEntry) {
    // Placeholder for production error tracking
    // Could integrate with Sentry, LogRocket, Datadog, etc.
    // Example:
    // if (window.Sentry) {
    //   window.Sentry.captureMessage(entry.message, entry.level);
    // }
  }

  getRecentLogs(level?: LogLevel): LogEntry[] {
    if (level) {
      return this.logs.filter((log) => log.level === level);
    }
    return [...this.logs];
  }

  clearLogs() {
    this.logs = [];
  }
}

export const logger = new Logger();

// Helper function to wrap async functions with error logging
export function withErrorLogging<T extends (...args: unknown[]) => Promise<unknown>>(
  fn: T,
  context: string
): (...args: Parameters<T>) => Promise<ReturnType<T>> {
  return async (...args: Parameters<T>): Promise<ReturnType<T>> => {
    try {
      return (await fn(...args)) as ReturnType<T>;
    } catch (error) {
      logger.error(`Error in ${context}`, { args }, error as Error);
      throw error;
    }
  };
}

// React component error handler
export function logComponentError(
  componentName: string,
  error: Error,
  errorInfo?: { componentStack?: string }
) {
  logger.error(`React error in ${componentName}`, {
    componentStack: errorInfo?.componentStack,
    stack: error.stack,
  }, error);
}
