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
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-50 to-indigo-100">
      <div className="max-w-4xl mx-auto px-4 text-center">
        <h1 className="text-6xl font-bold text-gray-900 mb-6">
          Hackathon Todo
        </h1>
        <p className="text-xl text-gray-600 mb-12">
          A modern task management application built with Next.js and FastAPI
        </p>

        <div className="flex gap-4 justify-center">
          <Link
            href="/login"
            className="bg-blue-600 text-white px-8 py-3 rounded-lg hover:bg-blue-700 transition font-medium text-lg"
          >
            Login
          </Link>
          <Link
            href="/register"
            className="bg-white text-blue-600 px-8 py-3 rounded-lg hover:bg-gray-50 transition font-medium text-lg border-2 border-blue-600"
          >
            Register
          </Link>
        </div>

        <div className="mt-16 grid grid-cols-1 md:grid-cols-3 gap-8">
          <div className="bg-white p-6 rounded-lg shadow-md">
            <h3 className="text-xl font-semibold text-gray-800 mb-2">Secure Authentication</h3>
            <p className="text-gray-600">JWT-based authentication to keep your tasks safe</p>
          </div>
          <div className="bg-white p-6 rounded-lg shadow-md">
            <h3 className="text-xl font-semibold text-gray-800 mb-2">Task Management</h3>
            <p className="text-gray-600">Create, update, and organize your tasks efficiently</p>
          </div>
          <div className="bg-white p-6 rounded-lg shadow-md">
            <h3 className="text-xl font-semibold text-gray-800 mb-2">Modern Stack</h3>
            <p className="text-gray-600">Built with Next.js, FastAPI, and PostgreSQL</p>
          </div>
        </div>
      </div>
    </div>
  );
}
