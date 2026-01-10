"use client";

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { useAuth } from '@/contexts/AuthContext';
import { chatAPI, ConversationResponse } from '@/lib/api';
import ChatUI from '@/components/ChatUI';
import Link from 'next/link';

export default function ChatPage() {
  const { isAuthenticated, logout } = useAuth();
  const router = useRouter();
  const [conversations, setConversations] = useState<ConversationResponse[]>([]);
  const [selectedConversation, setSelectedConversation] = useState<number | undefined>(undefined);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    if (!isAuthenticated) {
      router.push('/login');
      return;
    }
    loadConversations();
  }, [isAuthenticated, router]);

  const loadConversations = async () => {
    try {
      setLoading(true);
      const data = await chatAPI.getConversations();
      setConversations(data);
      setError('');
    } catch (err: any) {
      setError('Failed to load conversations');
    } finally {
      setLoading(false);
    }
  };

  const handleConversationCreated = (id: number) => {
    setSelectedConversation(id);
    // Reload conversations list
    loadConversations();
  };

  const handleDeleteConversation = async (id: number) => {
    try {
      await chatAPI.deleteConversation(id);
      setConversations((prev) => prev.filter((c) => c.id !== id));
      if (selectedConversation === id) {
        setSelectedConversation(undefined);
      }
    } catch (err) {
      setError('Failed to delete conversation');
    }
  };

  const handleLogout = async () => {
    logout();
    router.push('/');
  };

  return (
    <div className="min-h-screen bg-gray-50 flex flex-col">
      {/* Top Navigation */}
      <div className="bg-white shadow">
        <div className="max-w-7xl mx-auto px-4 py-4 flex justify-between items-center">
          <div>
            <h1 className="text-2xl font-bold text-gray-900">Chat with AI</h1>
            <p className="text-sm text-gray-600">Manage your tasks using natural language</p>
          </div>
          <div className="flex gap-4 items-center">
            <Link
              href="/tasks"
              className="text-gray-700 hover:text-gray-900 transition font-medium"
            >
              Tasks
            </Link>
            <button
              onClick={handleLogout}
              className="bg-red-600 text-white px-4 py-2 rounded hover:bg-red-700 transition font-medium"
            >
              Logout
            </button>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="flex-1 max-w-7xl mx-auto w-full grid grid-cols-1 lg:grid-cols-4 gap-6 p-6">
        {/* Sidebar - Conversations List */}
        <div className="lg:col-span-1 bg-white rounded-lg shadow-md p-4 h-fit">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">Conversations</h2>
          
          {loading ? (
            <div className="text-center py-4 text-gray-500">Loading...</div>
          ) : conversations.length === 0 ? (
            <div className="text-center py-4 text-gray-500">
              <p className="text-sm">No conversations yet</p>
              <p className="text-xs text-gray-400">Start chatting to create one</p>
            </div>
          ) : (
            <div className="space-y-2">
              {conversations.map((conv) => (
                <div
                  key={conv.id}
                  className={`p-3 rounded cursor-pointer transition flex items-center justify-between group ${
                    selectedConversation === conv.id
                      ? 'bg-blue-100 border border-blue-500'
                      : 'bg-gray-100 hover:bg-gray-200'
                  }`}
                >
                  <div
                    className="flex-1"
                    onClick={() => setSelectedConversation(conv.id)}
                  >
                    <p className="text-sm font-medium text-gray-900 truncate">
                      {conv.title || 'Untitled'}
                    </p>
                    <p className="text-xs text-gray-600 mt-1">
                      {conv.messages.length} messages
                    </p>
                  </div>
                  <button
                    onClick={(e) => {
                      e.stopPropagation();
                      handleDeleteConversation(conv.id);
                    }}
                    className="opacity-0 group-hover:opacity-100 text-red-600 hover:text-red-800 text-sm transition ml-2"
                  >
                    Delete
                  </button>
                </div>
              ))}
            </div>
          )}

          <button
            onClick={() => setSelectedConversation(undefined)}
            className="w-full mt-4 px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 transition font-medium text-sm"
          >
            New Chat
          </button>
        </div>

        {/* Main Chat Area */}
        <div className="lg:col-span-3">
          <ChatUI
            conversationId={selectedConversation}
            onConversationCreated={handleConversationCreated}
          />
        </div>
      </div>
    </div>
  );
}
