/**
 * Logger utility for consistent error logging across the application
 * In development: logs to console
 * In production: could be extended to send to error tracking service (Sentry, LogRocket, etc.)
 */

type LogLevel = 'debug' | 'info' | 'warn' | 'error';

interface LogEntry {
  level: LogLevel;
  message: string;
  timestamp: string;
  context?: Record<string, unknown>;
  error?: Error;
}

class Logger {
  private isDevelopment = import.meta.env.DEV;
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
