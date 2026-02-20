/**
 * Environment Configuration Module
 * 
 * This module provides type-safe access to environment variables
 * and validates them at runtime.
 * 
 * BEST PRACTICES:
 * 1. Always use this module instead of accessing process.env directly
 * 2. Validate required variables on app startup
 * 3. Provide sensible defaults for development
 * 4. Never expose secrets in NEXT_PUBLIC_ variables
 */

// Type for environment
type Environment = 'development' | 'staging' | 'production' | 'test';

/**
 * Public environment variables (accessible in browser)
 */
export const publicEnv = {
  apiUrl: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1',
  stripePublishableKey: process.env.NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY || '',
  gaId: process.env.NEXT_PUBLIC_GA_ID || '',
  sentryDsn: process.env.NEXT_PUBLIC_SENTRY_DSN || '',
  environment: (process.env.NEXT_PUBLIC_ENVIRONMENT || 'development') as Environment,
  appVersion: process.env.NEXT_PUBLIC_APP_VERSION || '1.0.0',
} as const;

/**
 * Server-only environment variables (NOT accessible in browser)
 * These will throw errors if accessed in client components
 */
export const serverEnv = {
  nextAuthUrl: process.env.NEXTAUTH_URL || 'http://localhost:3000',
  nextAuthSecret: process.env.NEXTAUTH_SECRET || '',
  databaseUrl: process.env.DATABASE_URL || '',
  stripeSecretKey: process.env.STRIPE_SECRET_KEY || '',
  openAiApiKey: process.env.OPENAI_API_KEY || '',
  sendGridApiKey: process.env.SENDGRID_API_KEY || '',
} as const;

/**
 * Node environment
 */
export const nodeEnv = process.env.NODE_ENV || 'development';

/**
 * Check if running in production
 */
export const isProduction = nodeEnv === 'production';

/**
 * Check if running in development
 */
export const isDevelopment = nodeEnv === 'development';

/**
 * Check if running in test
 */
export const isTest = nodeEnv === 'test';

/**
 * Check if running on server
 */
export const isServer = typeof window === 'undefined';

/**
 * Check if running on client
 */
export const isClient = typeof window !== 'undefined';

/**
 * Validate required environment variables
 * Call this in your root layout or app initialization
 */
export function validateEnv(): void {
  const errors: string[] = [];

  // Validate public variables
  if (isProduction && !publicEnv.apiUrl) {
    errors.push('NEXT_PUBLIC_API_URL is required in production');
  }

  // Validate server variables (only on server)
  if (isServer) {
    if (isProduction && !serverEnv.nextAuthSecret) {
      errors.push('NEXTAUTH_SECRET is required in production');
    }
    
    if (isProduction && serverEnv.nextAuthSecret.length < 32) {
      errors.push('NEXTAUTH_SECRET must be at least 32 characters');
    }
  }

  if (errors.length > 0) {
    console.error('Environment validation failed:');
    errors.forEach(error => console.error(`  - ${error}`));
    
    if (isProduction) {
      throw new Error('Environment validation failed. Check logs for details.');
    }
  }
}

/**
 * Get API URL with optional path
 */
export function getApiUrl(path: string = ''): string {
  const baseUrl = publicEnv.apiUrl.replace(/\/$/, ''); // Remove trailing slash
  const cleanPath = path.replace(/^\//, ''); // Remove leading slash
  return cleanPath ? `${baseUrl}/${cleanPath}` : baseUrl;
}

/**
 * Check if a feature flag is enabled
 */
export function isFeatureEnabled(feature: string): boolean {
  const envVar = process.env[`NEXT_PUBLIC_FEATURE_${feature.toUpperCase()}`];
  return envVar === 'true' || envVar === '1';
}

/**
 * Get environment-specific configuration
 */
export function getConfig() {
  return {
    // API Configuration
    api: {
      baseUrl: publicEnv.apiUrl,
      timeout: isDevelopment ? 30000 : 10000,
      retries: isProduction ? 3 : 1,
    },
    
    // Feature Flags
    features: {
      analytics: isProduction,
      errorTracking: isProduction,
      debugMode: isDevelopment,
    },
    
    // App Configuration
    app: {
      name: 'SkillProof AI',
      version: publicEnv.appVersion,
      environment: publicEnv.environment,
    },
  };
}

// Export a default config object
export const config = getConfig();
