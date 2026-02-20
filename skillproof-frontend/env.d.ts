/// <reference types="node" />

/**
 * Type definitions for Next.js environment variables
 * This file provides TypeScript autocomplete and type checking for process.env
 */

declare global {
  namespace NodeJS {
    interface ProcessEnv {
      // Public environment variables (accessible in browser)
      readonly NEXT_PUBLIC_API_URL: string;
      readonly NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY?: string;
      readonly NEXT_PUBLIC_GA_ID?: string;
      readonly NEXT_PUBLIC_SENTRY_DSN?: string;
      readonly NEXT_PUBLIC_ENVIRONMENT?: 'development' | 'staging' | 'production';
      readonly NEXT_PUBLIC_APP_VERSION?: string;
      
      // Server-only environment variables (NOT accessible in browser)
      readonly NEXTAUTH_URL?: string;
      readonly NEXTAUTH_SECRET?: string;
      readonly DATABASE_URL?: string;
      readonly STRIPE_SECRET_KEY?: string;
      readonly OPENAI_API_KEY?: string;
      readonly SENDGRID_API_KEY?: string;
      
      // Node environment
      readonly NODE_ENV: 'development' | 'production' | 'test';
    }
  }
}

export {};
