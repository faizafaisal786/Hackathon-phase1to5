"use client";

import { useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { useAuth } from '@/contexts/AuthContext';
import Link from 'next/link';

export default function HomePage() {
  const { isAuthenticated } = useAuth();
  const router = useRouter();

  useEffect(() => {
    if (isAuthenticated) {
      router.push('/tasks');
    }
  }, [isAuthenticated, router]);

  return (
    <div className="min-h-screen bg-gradient-to-br from-violet-600 via-purple-600 to-indigo-700">
      {/* Hero Section */}
      <div className="relative overflow-hidden">
        <div className="absolute inset-0 opacity-40" style={{backgroundImage: "radial-gradient(circle, rgba(255,255,255,0.1) 1px, transparent 1px)", backgroundSize: "20px 20px"}}></div>

        <div className="relative max-w-7xl mx-auto px-4 py-24 sm:py-32">
          <div className="text-center">
            <div className="inline-flex items-center px-4 py-2 bg-white/10 backdrop-blur-sm rounded-full text-white/90 text-sm font-medium mb-8">
              <span className="w-2 h-2 bg-green-400 rounded-full mr-2 animate-pulse"></span>
              Hackathon Phase 5 - Cloud Deployed
            </div>

            <h1 className="text-5xl md:text-7xl font-extrabold text-white mb-6 tracking-tight">
              AI-Powered
              <span className="block bg-gradient-to-r from-yellow-400 via-pink-400 to-cyan-400 text-transparent bg-clip-text">
                Todo App
              </span>
            </h1>

            <p className="text-xl md:text-2xl text-white/80 mb-12 max-w-3xl mx-auto">
              Manage tasks with natural language. Say
              <span className="text-yellow-300 font-semibold"> &quot;kal ka kaam add karo&quot; </span>
              or <span className="text-cyan-300 font-semibold">&quot;pending tasks dikhao&quot;</span>
            </p>

            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Link
                href="/login"
                className="group bg-white text-purple-700 px-8 py-4 rounded-xl hover:bg-yellow-400 hover:text-purple-900 transition-all font-bold text-lg shadow-xl hover:shadow-2xl hover:scale-105"
              >
                Get Started
                <span className="inline-block ml-2 group-hover:translate-x-1 transition-transform">→</span>
              </Link>
              <Link
                href="/register"
                className="bg-white/10 backdrop-blur-sm text-white px-8 py-4 rounded-xl hover:bg-white/20 transition-all font-bold text-lg border-2 border-white/30"
              >
                Create Account
              </Link>
            </div>
          </div>
        </div>
      </div>

      {/* Features Section */}
      <div className="bg-white py-24">
        <div className="max-w-7xl mx-auto px-4">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-bold text-gray-900 mb-4">Hackathon Features</h2>
            <p className="text-xl text-gray-600">All 5 phases completed with spec-driven development</p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {/* Phase 1 */}
            <div className="group bg-gradient-to-br from-green-50 to-emerald-100 p-8 rounded-2xl hover:shadow-xl transition-all hover:-translate-y-1">
              <div className="w-14 h-14 bg-green-500 rounded-xl flex items-center justify-center mb-6 group-hover:scale-110 transition-transform">
                <span className="text-2xl">✓</span>
              </div>
              <h3 className="text-xl font-bold text-gray-900 mb-3">Phase 1: Console App</h3>
              <p className="text-gray-600">Python CLI with Add, Update, Delete, View, Complete tasks</p>
              <span className="inline-block mt-4 text-green-600 font-semibold text-sm">100 Points ✓</span>
            </div>

            {/* Phase 2 */}
            <div className="group bg-gradient-to-br from-blue-50 to-indigo-100 p-8 rounded-2xl hover:shadow-xl transition-all hover:-translate-y-1">
              <div className="w-14 h-14 bg-blue-500 rounded-xl flex items-center justify-center mb-6 group-hover:scale-110 transition-transform">
                <span className="text-2xl">🌐</span>
              </div>
              <h3 className="text-xl font-bold text-gray-900 mb-3">Phase 2: Full-Stack Web</h3>
              <p className="text-gray-600">Next.js Frontend + FastAPI Backend + Auth</p>
              <span className="inline-block mt-4 text-blue-600 font-semibold text-sm">150 Points ✓</span>
            </div>

            {/* Phase 3 */}
            <div className="group bg-gradient-to-br from-purple-50 to-violet-100 p-8 rounded-2xl hover:shadow-xl transition-all hover:-translate-y-1">
              <div className="w-14 h-14 bg-purple-500 rounded-xl flex items-center justify-center mb-6 group-hover:scale-110 transition-transform">
                <span className="text-2xl">🤖</span>
              </div>
              <h3 className="text-xl font-bold text-gray-900 mb-3">Phase 3: AI Chatbot</h3>
              <p className="text-gray-600">Natural language commands in English, Hindi & Urdu</p>
              <span className="inline-block mt-4 text-purple-600 font-semibold text-sm">200 Points ✓</span>
            </div>

            {/* Phase 4 */}
            <div className="group bg-gradient-to-br from-orange-50 to-amber-100 p-8 rounded-2xl hover:shadow-xl transition-all hover:-translate-y-1">
              <div className="w-14 h-14 bg-orange-500 rounded-xl flex items-center justify-center mb-6 group-hover:scale-110 transition-transform">
                <span className="text-2xl">☸️</span>
              </div>
              <h3 className="text-xl font-bold text-gray-900 mb-3">Phase 4: Kubernetes</h3>
              <p className="text-gray-600">Docker + Minikube + Helm Charts ready</p>
              <span className="inline-block mt-4 text-orange-600 font-semibold text-sm">250 Points ✓</span>
            </div>

            {/* Phase 5 */}
            <div className="group bg-gradient-to-br from-pink-50 to-rose-100 p-8 rounded-2xl hover:shadow-xl transition-all hover:-translate-y-1">
              <div className="w-14 h-14 bg-pink-500 rounded-xl flex items-center justify-center mb-6 group-hover:scale-110 transition-transform">
                <span className="text-2xl">☁️</span>
              </div>
              <h3 className="text-xl font-bold text-gray-900 mb-3">Phase 5: Cloud Deploy</h3>
              <p className="text-gray-600">Vercel deployment with CI/CD + Event-driven</p>
              <span className="inline-block mt-4 text-pink-600 font-semibold text-sm">300 Points ✓</span>
            </div>

            {/* Bonus */}
            <div className="group bg-gradient-to-br from-cyan-50 to-teal-100 p-8 rounded-2xl hover:shadow-xl transition-all hover:-translate-y-1">
              <div className="w-14 h-14 bg-gradient-to-r from-cyan-500 to-teal-500 rounded-xl flex items-center justify-center mb-6 group-hover:scale-110 transition-transform">
                <span className="text-2xl">🎁</span>
              </div>
              <h3 className="text-xl font-bold text-gray-900 mb-3">Bonus Features</h3>
              <p className="text-gray-600">Urdu/Hindi support, Priority, Tags, Due dates</p>
              <span className="inline-block mt-4 text-teal-600 font-semibold text-sm">+100 Bonus ✓</span>
            </div>
          </div>
        </div>
      </div>

      {/* Tech Stack */}
      <div className="bg-gray-900 py-16">
        <div className="max-w-7xl mx-auto px-4">
          <h3 className="text-center text-white/60 text-sm font-semibold uppercase tracking-wider mb-8">
            Built With Modern Tech Stack
          </h3>
          <div className="flex flex-wrap justify-center items-center gap-8 md:gap-16">
            <div className="text-white/80 font-bold text-lg">Next.js 14</div>
            <div className="text-white/80 font-bold text-lg">FastAPI</div>
            <div className="text-white/80 font-bold text-lg">Python</div>
            <div className="text-white/80 font-bold text-lg">TypeScript</div>
            <div className="text-white/80 font-bold text-lg">Tailwind CSS</div>
            <div className="text-white/80 font-bold text-lg">Vercel</div>
          </div>
        </div>
      </div>

      {/* Footer */}
      <div className="bg-gradient-to-r from-purple-900 to-indigo-900 py-8">
        <div className="max-w-7xl mx-auto px-4 text-center">
          <p className="text-white/60 text-sm">
            Hackathon II - Spec-Driven Development | Built with AI Assistance
          </p>
        </div>
      </div>
    </div>
  );
}
