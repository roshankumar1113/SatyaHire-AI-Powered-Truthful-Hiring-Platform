import { Inter } from 'next/font/google';
import { AuthProvider } from '@/context/AuthContext';
import { validateEnv } from '@/lib/env';
import './globals.css';

const inter = Inter({ subsets: ['latin'] });

// Validate environment variables on app startup
// This will throw an error in production if required variables are missing
if (process.env.NODE_ENV !== 'test') {
  validateEnv();
}

export const metadata = {
  title: 'SkillProof AI - AI-Powered Skill Verification',
  description: 'Transform your hiring process with AI-powered skill verification and fraud detection',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className={inter.className}>
        <AuthProvider>
          {children}
        </AuthProvider>
      </body>
    </html>
  );
}
