'use client';

import Link from 'next/link';
import { Shield, ArrowLeft, CheckCircle } from 'lucide-react';

export default function DashboardPage() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900">
      <div className="container mx-auto px-6 py-12">
        {/* Header */}
        <div className="flex items-center justify-between mb-8">
          <div className="flex items-center gap-3">
            <Shield className="h-8 w-8 text-purple-400" />
            <h1 className="text-2xl font-bold text-white">SkillProof AI</h1>
          </div>
          <Link 
            href="/"
            className="text-gray-300 hover:text-white transition flex items-center gap-2"
          >
            <ArrowLeft className="h-4 w-4" />
            Back to Home
          </Link>
        </div>

        {/* Success Message */}
        <div className="max-w-2xl mx-auto">
          <div className="bg-white/10 backdrop-blur-lg rounded-2xl border border-white/20 p-8 text-center">
            <div className="flex justify-center mb-6">
              <div className="h-16 w-16 bg-green-500/20 rounded-full flex items-center justify-center">
                <CheckCircle className="h-10 w-10 text-green-400" />
              </div>
            </div>
            
            <h2 className="text-3xl font-bold text-white mb-4">
              Welcome to SkillProof AI! 🎉
            </h2>
            
            <p className="text-gray-300 mb-6">
              You've successfully logged in. Your dashboard is being prepared.
            </p>

            <div className="bg-purple-500/20 border border-purple-500/30 rounded-lg p-6 mb-6">
              <h3 className="text-white font-semibold mb-3">What's Next?</h3>
              <ul className="text-left text-gray-300 space-y-2">
                <li className="flex items-start gap-2">
                  <CheckCircle className="h-5 w-5 text-green-400 mt-0.5 flex-shrink-0" />
                  <span>Complete your profile</span>
                </li>
                <li className="flex items-start gap-2">
                  <CheckCircle className="h-5 w-5 text-green-400 mt-0.5 flex-shrink-0" />
                  <span>Upload your resume (for candidates)</span>
                </li>
                <li className="flex items-start gap-2">
                  <CheckCircle className="h-5 w-5 text-green-400 mt-0.5 flex-shrink-0" />
                  <span>Create your first job posting (for companies)</span>
                </li>
                <li className="flex items-start gap-2">
                  <CheckCircle className="h-5 w-5 text-green-400 mt-0.5 flex-shrink-0" />
                  <span>Explore AI-powered features</span>
                </li>
              </ul>
            </div>

            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Link
                href="/"
                className="px-6 py-3 bg-gradient-to-r from-purple-600 to-pink-600 text-white rounded-lg font-semibold hover:shadow-lg hover:shadow-purple-500/50 transition"
              >
                Explore Features
              </Link>
              <button
                onClick={() => alert('Logout functionality will be implemented with backend')}
                className="px-6 py-3 bg-white/10 text-white rounded-lg font-semibold hover:bg-white/20 transition border border-white/20"
              >
                Logout
              </button>
            </div>
          </div>

          {/* Info Box */}
          <div className="mt-8 bg-blue-500/20 border border-blue-500/30 rounded-lg p-4">
            <p className="text-blue-200 text-sm text-center">
              <strong>Note:</strong> This is a demo dashboard. Full functionality will be available once you connect the backend API.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
