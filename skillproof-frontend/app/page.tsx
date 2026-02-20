import Link from 'next/link';
import { ArrowRight, Shield, Brain, Zap, CheckCircle, TrendingUp, Users, Camera } from 'lucide-react';

export default function Home() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900">
      {/* Navigation */}
      <nav className="container mx-auto px-6 py-6">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-2">
            <Shield className="h-8 w-8 text-purple-400" />
            <span className="text-2xl font-bold text-white">SkillProof AI</span>
          </div>
          <div className="hidden md:flex items-center space-x-8">
            <Link href="#features" className="text-gray-300 hover:text-white transition">
              Features
            </Link>
            <Link href="#how-it-works" className="text-gray-300 hover:text-white transition">
              How It Works
            </Link>
            <Link href="#pricing" className="text-gray-300 hover:text-white transition">
              Pricing
            </Link>
            <Link 
              href="/login" 
              className="px-6 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700 transition"
            >
              Sign In
            </Link>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="container mx-auto px-6 py-20 text-center">
        <div className="max-w-4xl mx-auto">
          <div className="inline-block mb-4 px-4 py-2 bg-purple-500/20 rounded-full border border-purple-500/30">
            <span className="text-purple-300 text-sm font-semibold">
              🚀 AI-Powered Hiring Intelligence
            </span>
          </div>
          
          <h1 className="text-5xl md:text-7xl font-bold text-white mb-6 leading-tight">
            Stop Hiring Liars.
            <br />
            <span className="text-transparent bg-clip-text bg-gradient-to-r from-purple-400 to-pink-400">
              Start Hiring Talent.
            </span>
          </h1>
          
          <p className="text-xl text-gray-300 mb-8 max-w-2xl mx-auto">
            Transform your hiring with AI-powered interviews, skill verification, and fraud detection. 
            Our AI agent conducts live video interviews and analyzes candidates in real-time.
          </p>
          
          <div className="flex flex-col sm:flex-row gap-4 justify-center items-center">
            <Link 
              href="/signup" 
              className="px-8 py-4 bg-gradient-to-r from-purple-600 to-pink-600 text-white rounded-lg font-semibold hover:shadow-lg hover:shadow-purple-500/50 transition-all flex items-center gap-2 group"
            >
              Start Free Trial
              <ArrowRight className="h-5 w-5 group-hover:translate-x-1 transition-transform" />
            </Link>
            <Link 
              href="/login" 
              className="px-8 py-4 bg-white/10 text-white rounded-lg font-semibold hover:bg-white/20 transition backdrop-blur-sm border border-white/20"
            >
              Sign In
            </Link>
          </div>

          {/* Stats */}
          <div className="grid grid-cols-3 gap-8 mt-16 max-w-3xl mx-auto">
            <div className="text-center">
              <div className="text-4xl font-bold text-white mb-2">85%</div>
              <div className="text-gray-400 text-sm">Resume Fraud Detected</div>
            </div>
            <div className="text-center">
              <div className="text-4xl font-bold text-white mb-2">80%</div>
              <div className="text-gray-400 text-sm">Time Saved</div>
            </div>
            <div className="text-center">
              <div className="text-4xl font-bold text-white mb-2">90%</div>
              <div className="text-gray-400 text-sm">Accuracy Rate</div>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section id="features" className="container mx-auto px-6 py-20">
        <div className="text-center mb-16">
          <h2 className="text-4xl font-bold text-white mb-4">
            Powerful Features for Modern Hiring
          </h2>
          <p className="text-gray-400 text-lg">
            Everything you need to make better hiring decisions, faster.
          </p>
        </div>

        <div className="grid md:grid-cols-3 gap-8">
          {/* Feature 1 - AI Interview Agent */}
          <div className="bg-white/5 backdrop-blur-sm border border-white/10 rounded-2xl p-8 hover:bg-white/10 transition">
            <div className="h-12 w-12 bg-gradient-to-br from-purple-500 to-pink-500 rounded-lg flex items-center justify-center mb-6">
              <Camera className="h-6 w-6 text-white" />
            </div>
            <h3 className="text-xl font-bold text-white mb-3">AI Interview Agent</h3>
            <p className="text-gray-400 mb-4">
              Our AI agent conducts live video interviews, asks relevant questions, and analyzes responses in real-time.
            </p>
            <ul className="space-y-2">
              <li className="flex items-center text-gray-300 text-sm">
                <CheckCircle className="h-4 w-4 text-green-400 mr-2" />
                Live video interviews
              </li>
              <li className="flex items-center text-gray-300 text-sm">
                <CheckCircle className="h-4 w-4 text-green-400 mr-2" />
                Natural conversation flow
              </li>
              <li className="flex items-center text-gray-300 text-sm">
                <CheckCircle className="h-4 w-4 text-green-400 mr-2" />
                Real-time analysis
              </li>
            </ul>
          </div>

          {/* Feature 2 */}
          <div className="bg-white/5 backdrop-blur-sm border border-white/10 rounded-2xl p-8 hover:bg-white/10 transition">
            <div className="h-12 w-12 bg-purple-500/20 rounded-lg flex items-center justify-center mb-6">
              <Brain className="h-6 w-6 text-purple-400" />
            </div>
            <h3 className="text-xl font-bold text-white mb-3">AI Resume Parser</h3>
            <p className="text-gray-400 mb-4">
              Extract skills, experience, and qualifications from resumes in seconds with 85% accuracy.
            </p>
            <ul className="space-y-2">
              <li className="flex items-center text-gray-300 text-sm">
                <CheckCircle className="h-4 w-4 text-green-400 mr-2" />
                PDF & DOCX support
              </li>
              <li className="flex items-center text-gray-300 text-sm">
                <CheckCircle className="h-4 w-4 text-green-400 mr-2" />
                NLP-powered extraction
              </li>
              <li className="flex items-center text-gray-300 text-sm">
                <CheckCircle className="h-4 w-4 text-green-400 mr-2" />
                Instant skill matching
              </li>
            </ul>
          </div>

          {/* Feature 3 */}
          <div className="bg-white/5 backdrop-blur-sm border border-white/10 rounded-2xl p-8 hover:bg-white/10 transition">
            <div className="h-12 w-12 bg-pink-500/20 rounded-lg flex items-center justify-center mb-6">
              <Shield className="h-6 w-6 text-pink-400" />
            </div>
            <h3 className="text-xl font-bold text-white mb-3">Fraud Detection</h3>
            <p className="text-gray-400 mb-4">
              Real-time monitoring detects cheating, tab switches, and suspicious behavior with 90% accuracy.
            </p>
            <ul className="space-y-2">
              <li className="flex items-center text-gray-300 text-sm">
                <CheckCircle className="h-4 w-4 text-green-400 mr-2" />
                Tab switch tracking
              </li>
              <li className="flex items-center text-gray-300 text-sm">
                <CheckCircle className="h-4 w-4 text-green-400 mr-2" />
                Time anomaly detection
              </li>
              <li className="flex items-center text-gray-300 text-sm">
                <CheckCircle className="h-4 w-4 text-green-400 mr-2" />
                Explainable AI scores
              </li>
            </ul>
          </div>
        </div>
      </section>

      {/* How It Works */}
      <section id="how-it-works" className="container mx-auto px-6 py-20">
        <div className="text-center mb-16">
          <h2 className="text-4xl font-bold text-white mb-4">
            How It Works
          </h2>
          <p className="text-gray-400 text-lg">
            Get started in 3 simple steps
          </p>
        </div>

        <div className="grid md:grid-cols-3 gap-8 max-w-5xl mx-auto">
          <div className="text-center">
            <div className="h-16 w-16 bg-gradient-to-br from-purple-500 to-pink-500 rounded-full flex items-center justify-center mx-auto mb-6 text-2xl font-bold text-white">
              1
            </div>
            <h3 className="text-xl font-bold text-white mb-3">Upload Job Description</h3>
            <p className="text-gray-400">
              Paste your job requirements and let AI extract the required skills.
            </p>
          </div>

          <div className="text-center">
            <div className="h-16 w-16 bg-gradient-to-br from-purple-500 to-pink-500 rounded-full flex items-center justify-center mx-auto mb-6 text-2xl font-bold text-white">
              2
            </div>
            <h3 className="text-xl font-bold text-white mb-3">AI Generates Tests</h3>
            <p className="text-gray-400">
              Custom assessments are created automatically based on the role.
            </p>
          </div>

          <div className="text-center">
            <div className="h-16 w-16 bg-gradient-to-br from-purple-500 to-pink-500 rounded-full flex items-center justify-center mx-auto mb-6 text-2xl font-bold text-white">
              3
            </div>
            <h3 className="text-xl font-bold text-white mb-3">Get Verified Results</h3>
            <p className="text-gray-400">
              Receive fraud-checked scores with detailed analytics and insights.
            </p>
          </div>
        </div>
      </section>

      {/* Pricing Section */}
      <section id="pricing" className="container mx-auto px-6 py-20">
        <div className="text-center mb-16">
          <h2 className="text-4xl font-bold text-white mb-4">
            Simple, Transparent Pricing
          </h2>
          <p className="text-gray-400 text-lg">
            Choose the plan that fits your hiring needs
          </p>
        </div>

        <div className="grid md:grid-cols-3 gap-8 max-w-6xl mx-auto">
          {/* Starter Plan */}
          <div className="bg-white/5 backdrop-blur-sm border border-white/10 rounded-2xl p-8 hover:bg-white/10 transition">
            <div className="mb-6">
              <h3 className="text-2xl font-bold text-white mb-2">Starter</h3>
              <p className="text-gray-400 text-sm">Perfect for small teams</p>
            </div>
            <div className="mb-6">
              <div className="flex items-baseline">
                <span className="text-5xl font-bold text-white">$49</span>
                <span className="text-gray-400 ml-2">/month</span>
              </div>
              <p className="text-gray-500 text-sm mt-2">Billed monthly</p>
            </div>
            <ul className="space-y-4 mb-8">
              <li className="flex items-start text-gray-300">
                <CheckCircle className="h-5 w-5 text-green-400 mr-3 mt-0.5 flex-shrink-0" />
                <span>Up to 50 assessments/month</span>
              </li>
              <li className="flex items-start text-gray-300">
                <CheckCircle className="h-5 w-5 text-green-400 mr-3 mt-0.5 flex-shrink-0" />
                <span>AI Resume Parser</span>
              </li>
              <li className="flex items-start text-gray-300">
                <CheckCircle className="h-5 w-5 text-green-400 mr-3 mt-0.5 flex-shrink-0" />
                <span>Basic fraud detection</span>
              </li>
              <li className="flex items-start text-gray-300">
                <CheckCircle className="h-5 w-5 text-green-400 mr-3 mt-0.5 flex-shrink-0" />
                <span>Email support</span>
              </li>
              <li className="flex items-start text-gray-300">
                <CheckCircle className="h-5 w-5 text-green-400 mr-3 mt-0.5 flex-shrink-0" />
                <span>5 team members</span>
              </li>
            </ul>
            <Link 
              href="/signup" 
              className="block w-full py-3 px-6 bg-white/10 text-white rounded-lg font-semibold hover:bg-white/20 transition text-center border border-white/20"
            >
              Start Free Trial
            </Link>
          </div>

          {/* Professional Plan - Popular */}
          <div className="bg-gradient-to-br from-purple-600/20 to-pink-600/20 backdrop-blur-sm border-2 border-purple-500 rounded-2xl p-8 relative transform scale-105 shadow-2xl shadow-purple-500/20">
            <div className="absolute -top-4 left-1/2 transform -translate-x-1/2">
              <span className="bg-gradient-to-r from-purple-600 to-pink-600 text-white px-4 py-1 rounded-full text-sm font-semibold">
                Most Popular
              </span>
            </div>
            <div className="mb-6">
              <h3 className="text-2xl font-bold text-white mb-2">Professional</h3>
              <p className="text-gray-300 text-sm">For growing companies</p>
            </div>
            <div className="mb-6">
              <div className="flex items-baseline">
                <span className="text-5xl font-bold text-white">$149</span>
                <span className="text-gray-300 ml-2">/month</span>
              </div>
              <p className="text-gray-400 text-sm mt-2">Billed monthly</p>
            </div>
            <ul className="space-y-4 mb-8">
              <li className="flex items-start text-white">
                <CheckCircle className="h-5 w-5 text-green-400 mr-3 mt-0.5 flex-shrink-0" />
                <span>Up to 200 assessments/month</span>
              </li>
              <li className="flex items-start text-white">
                <CheckCircle className="h-5 w-5 text-green-400 mr-3 mt-0.5 flex-shrink-0" />
                <span>AI Resume Parser + Skill Matching</span>
              </li>
              <li className="flex items-start text-white">
                <CheckCircle className="h-5 w-5 text-green-400 mr-3 mt-0.5 flex-shrink-0" />
                <span>Advanced fraud detection</span>
              </li>
              <li className="flex items-start text-white">
                <CheckCircle className="h-5 w-5 text-green-400 mr-3 mt-0.5 flex-shrink-0" />
                <span>Camera monitoring</span>
              </li>
              <li className="flex items-start text-white">
                <CheckCircle className="h-5 w-5 text-green-400 mr-3 mt-0.5 flex-shrink-0" />
                <span>Priority support</span>
              </li>
              <li className="flex items-start text-white">
                <CheckCircle className="h-5 w-5 text-green-400 mr-3 mt-0.5 flex-shrink-0" />
                <span>20 team members</span>
              </li>
              <li className="flex items-start text-white">
                <CheckCircle className="h-5 w-5 text-green-400 mr-3 mt-0.5 flex-shrink-0" />
                <span>Custom branding</span>
              </li>
            </ul>
            <Link 
              href="/signup" 
              className="block w-full py-3 px-6 bg-gradient-to-r from-purple-600 to-pink-600 text-white rounded-lg font-semibold hover:shadow-lg hover:shadow-purple-500/50 transition text-center"
            >
              Start Free Trial
            </Link>
          </div>

          {/* Enterprise Plan */}
          <div className="bg-white/5 backdrop-blur-sm border border-white/10 rounded-2xl p-8 hover:bg-white/10 transition">
            <div className="mb-6">
              <h3 className="text-2xl font-bold text-white mb-2">Enterprise</h3>
              <p className="text-gray-400 text-sm">For large organizations</p>
            </div>
            <div className="mb-6">
              <div className="flex items-baseline">
                <span className="text-5xl font-bold text-white">Custom</span>
              </div>
              <p className="text-gray-500 text-sm mt-2">Contact for pricing</p>
            </div>
            <ul className="space-y-4 mb-8">
              <li className="flex items-start text-gray-300">
                <CheckCircle className="h-5 w-5 text-green-400 mr-3 mt-0.5 flex-shrink-0" />
                <span>Unlimited assessments</span>
              </li>
              <li className="flex items-start text-gray-300">
                <CheckCircle className="h-5 w-5 text-green-400 mr-3 mt-0.5 flex-shrink-0" />
                <span>All Professional features</span>
              </li>
              <li className="flex items-start text-gray-300">
                <CheckCircle className="h-5 w-5 text-green-400 mr-3 mt-0.5 flex-shrink-0" />
                <span>Dedicated account manager</span>
              </li>
              <li className="flex items-start text-gray-300">
                <CheckCircle className="h-5 w-5 text-green-400 mr-3 mt-0.5 flex-shrink-0" />
                <span>Custom integrations</span>
              </li>
              <li className="flex items-start text-gray-300">
                <CheckCircle className="h-5 w-5 text-green-400 mr-3 mt-0.5 flex-shrink-0" />
                <span>SLA guarantee</span>
              </li>
              <li className="flex items-start text-gray-300">
                <CheckCircle className="h-5 w-5 text-green-400 mr-3 mt-0.5 flex-shrink-0" />
                <span>Unlimited team members</span>
              </li>
              <li className="flex items-start text-gray-300">
                <CheckCircle className="h-5 w-5 text-green-400 mr-3 mt-0.5 flex-shrink-0" />
                <span>On-premise deployment</span>
              </li>
            </ul>
            <Link 
              href="/contact" 
              className="block w-full py-3 px-6 bg-white/10 text-white rounded-lg font-semibold hover:bg-white/20 transition text-center border border-white/20"
            >
              Contact Sales
            </Link>
          </div>
        </div>

        {/* Pricing FAQ */}
        <div className="mt-16 text-center">
          <p className="text-gray-400 mb-4">
            All plans include 14-day free trial. No credit card required.
          </p>
          <div className="flex flex-wrap justify-center gap-6 text-sm">
            <div className="flex items-center text-gray-300">
              <CheckCircle className="h-4 w-4 text-green-400 mr-2" />
              Cancel anytime
            </div>
            <div className="flex items-center text-gray-300">
              <CheckCircle className="h-4 w-4 text-green-400 mr-2" />
              No setup fees
            </div>
            <div className="flex items-center text-gray-300">
              <CheckCircle className="h-4 w-4 text-green-400 mr-2" />
              24/7 support
            </div>
          </div>
        </div>
      </section>

      {/* Social Proof */}
      <section className="container mx-auto px-6 py-20">
        <div className="bg-gradient-to-r from-purple-500/10 to-pink-500/10 backdrop-blur-sm border border-white/10 rounded-3xl p-12 text-center">
          <div className="flex items-center justify-center gap-2 mb-6">
            <Users className="h-8 w-8 text-purple-400" />
            <TrendingUp className="h-8 w-8 text-pink-400" />
          </div>
          <h2 className="text-3xl font-bold text-white mb-4">
            Trusted by 150+ Companies
          </h2>
          <p className="text-gray-300 text-lg mb-8 max-w-2xl mx-auto">
            From startups to enterprises, companies are using SkillProof AI to make better hiring decisions.
          </p>
          <div className="flex flex-wrap justify-center gap-4">
            <div className="px-6 py-3 bg-white/5 rounded-lg border border-white/10">
              <span className="text-white font-semibold">10,000+</span>
              <span className="text-gray-400 ml-2">Assessments</span>
            </div>
            <div className="px-6 py-3 bg-white/5 rounded-lg border border-white/10">
              <span className="text-white font-semibold">50,000+</span>
              <span className="text-gray-400 ml-2">Hours Saved</span>
            </div>
            <div className="px-6 py-3 bg-white/5 rounded-lg border border-white/10">
              <span className="text-white font-semibold">1,200+</span>
              <span className="text-gray-400 ml-2">Frauds Detected</span>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="container mx-auto px-6 py-20">
        <div className="bg-gradient-to-r from-purple-600 to-pink-600 rounded-3xl p-12 text-center">
          <h2 className="text-4xl font-bold text-white mb-4">
            Ready to Transform Your Hiring?
          </h2>
          <p className="text-white/90 text-lg mb-8 max-w-2xl mx-auto">
            Join 150+ companies using AI to hire better, faster, and smarter.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link 
              href="/signup" 
              className="px-8 py-4 bg-white text-purple-600 rounded-lg font-semibold hover:bg-gray-100 transition"
            >
              Start Free Trial
            </Link>
            <Link 
              href="/contact" 
              className="px-8 py-4 bg-white/10 text-white rounded-lg font-semibold hover:bg-white/20 transition backdrop-blur-sm border border-white/20"
            >
              Talk to Sales
            </Link>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="container mx-auto px-6 py-12 border-t border-white/10">
        <div className="grid md:grid-cols-4 gap-8 mb-8">
          <div>
            <div className="flex items-center space-x-2 mb-4">
              <Shield className="h-6 w-6 text-purple-400" />
              <span className="text-xl font-bold text-white">SkillProof AI</span>
            </div>
            <p className="text-gray-400 text-sm">
              AI-powered skill verification and hiring intelligence platform.
            </p>
          </div>
          
          <div>
            <h4 className="text-white font-semibold mb-4">Product</h4>
            <ul className="space-y-2">
              <li><Link href="/features" className="text-gray-400 hover:text-white text-sm">Features</Link></li>
              <li><Link href="/pricing" className="text-gray-400 hover:text-white text-sm">Pricing</Link></li>
              <li><Link href="/demo" className="text-gray-400 hover:text-white text-sm">Demo</Link></li>
            </ul>
          </div>
          
          <div>
            <h4 className="text-white font-semibold mb-4">Company</h4>
            <ul className="space-y-2">
              <li><Link href="/about" className="text-gray-400 hover:text-white text-sm">About</Link></li>
              <li><Link href="/blog" className="text-gray-400 hover:text-white text-sm">Blog</Link></li>
              <li><Link href="/careers" className="text-gray-400 hover:text-white text-sm">Careers</Link></li>
            </ul>
          </div>
          
          <div>
            <h4 className="text-white font-semibold mb-4">Legal</h4>
            <ul className="space-y-2">
              <li><Link href="/privacy" className="text-gray-400 hover:text-white text-sm">Privacy</Link></li>
              <li><Link href="/terms" className="text-gray-400 hover:text-white text-sm">Terms</Link></li>
              <li><Link href="/security" className="text-gray-400 hover:text-white text-sm">Security</Link></li>
            </ul>
          </div>
        </div>
        
        <div className="border-t border-white/10 pt-8 text-center text-gray-400 text-sm">
          <p>© 2026 SkillProof AI. All rights reserved. Built with ❤️ in India 🇮🇳</p>
        </div>
      </footer>
    </div>
  );
}
