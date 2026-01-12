"use client";

import { useEffect, useState } from 'react';
import axios from 'axios';

export default function TestPage() {
  const [apiUrl, setApiUrl] = useState('');
  const [envVar, setEnvVar] = useState('');
  const [backendStatus, setBackendStatus] = useState('Checking...');
  const [error, setError] = useState('');

  useEffect(() => {
    // Check environment variable
    const url = process.env.NEXT_PUBLIC_API_URL || 'NOT SET';
    setEnvVar(url);

    // Get actual API URL being used
    const actualUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
    setApiUrl(actualUrl);

    // Test backend connection
    const testBackend = async () => {
      try {
        const response = await axios.get(`${actualUrl}/`, { timeout: 5000 });
        setBackendStatus('✅ Connected! Backend is working.');
      } catch (err: any) {
        setBackendStatus('❌ Cannot connect to backend');
        setError(err.message || 'Connection failed');
      }
    };

    testBackend();
  }, []);

  return (
    <div className="min-h-screen bg-gray-100 p-8">
      <div className="max-w-4xl mx-auto">
        <h1 className="text-3xl font-bold mb-6">🔍 Deployment Diagnostics</h1>

        <div className="bg-white rounded-lg shadow p-6 mb-4">
          <h2 className="text-xl font-semibold mb-4">Environment Configuration</h2>
          <div className="space-y-2">
            <div className="flex">
              <span className="font-medium w-48">NEXT_PUBLIC_API_URL:</span>
              <span className={envVar === 'NOT SET' ? 'text-red-600 font-bold' : 'text-green-600'}>
                {envVar}
              </span>
            </div>
            <div className="flex">
              <span className="font-medium w-48">Current API URL:</span>
              <span className="text-blue-600">{apiUrl}</span>
            </div>
          </div>
        </div>

        <div className="bg-white rounded-lg shadow p-6 mb-4">
          <h2 className="text-xl font-semibold mb-4">Backend Connection Test</h2>
          <div className="space-y-2">
            <p><strong>Status:</strong> {backendStatus}</p>
            {error && (
              <p className="text-red-600"><strong>Error:</strong> {error}</p>
            )}
          </div>
        </div>

        <div className="bg-yellow-50 border-l-4 border-yellow-400 p-6 mb-4">
          <h3 className="font-bold text-lg mb-2">⚠️ If Backend Connection Failed:</h3>
          <ol className="list-decimal list-inside space-y-2">
            <li>Make sure your backend is deployed to Vercel</li>
            <li>Go to Vercel Dashboard → Your Frontend Project</li>
            <li>Go to Settings → Environment Variables</li>
            <li>Add: <code className="bg-gray-200 px-2 py-1 rounded">NEXT_PUBLIC_API_URL</code> = Your backend URL</li>
            <li>Redeploy your frontend</li>
          </ol>
        </div>

        <div className="bg-blue-50 border-l-4 border-blue-400 p-6">
          <h3 className="font-bold text-lg mb-2">📝 Quick Fix Steps:</h3>
          <ol className="list-decimal list-inside space-y-2 text-sm">
            <li><strong>Deploy Backend First:</strong>
              <ul className="list-disc list-inside ml-6 mt-1">
                <li>Go to Vercel → Import Project</li>
                <li>Root Directory: <code className="bg-white px-2 py-1 rounded">hackathon-todo/backend</code></li>
                <li>Add env var: <code className="bg-white px-2 py-1 rounded">OPENAI_API_KEY=demo</code></li>
                <li>Copy the deployed URL</li>
              </ul>
            </li>
            <li><strong>Update Frontend Env Var:</strong>
              <ul className="list-disc list-inside ml-6 mt-1">
                <li>Frontend Settings → Environment Variables</li>
                <li>Add: <code className="bg-white px-2 py-1 rounded">NEXT_PUBLIC_API_URL</code> = Backend URL</li>
                <li>Click Redeploy</li>
              </ul>
            </li>
          </ol>
        </div>

        <div className="mt-6 text-center">
          <a href="/" className="text-blue-600 hover:underline">← Back to Home</a>
        </div>
      </div>
    </div>
  );
}
