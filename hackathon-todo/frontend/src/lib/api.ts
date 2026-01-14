/**
 * API client for backend communication
 */
import axios from 'axios';

// API URL configuration
const getApiUrl = () => {
  // If environment variable is set, use it
  if (process.env.NEXT_PUBLIC_API_URL) {
    return process.env.NEXT_PUBLIC_API_URL;
  }

  // Production backend URL (Vercel deployed)
  return 'https://backend-flax-seven-28.vercel.app';
};

const API_URL = getApiUrl();

export const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add token to requests
api.interceptors.request.use((config) => {
  // Check if we're on the client side before accessing localStorage
  if (typeof window !== 'undefined') {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
  }
  return config;
});

// Handle 401 responses
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Check if we're on the client side before accessing localStorage and window
      if (typeof window !== 'undefined') {
        localStorage.removeItem('token');
        window.location.href = '/login';
      }
    }
    return Promise.reject(error);
  }
);

export interface User {
  id: number;
  email: string;
  username: string;
  full_name?: string;
  is_active: boolean;
  created_at: string;
}

export interface Task {
  id: number;
  title: string;
  description?: string;
  completed: boolean;
  owner_id: number;
  created_at: string;
  updated_at: string;
}

export interface TaskCreate {
  title: string;
  description?: string;
  completed?: boolean;
}

export interface TaskUpdate {
  title?: string;
  description?: string;
  completed?: boolean;
}

export const authAPI = {
  register: async (email: string, username: string, password: string, full_name?: string) => {
    const response = await api.post<User>('/auth/register', {
      email,
      username,
      password,
      full_name,
    });
    return response.data;
  },

  login: async (username: string, password: string) => {
    const response = await api.post<{ access_token: string; token_type: string }>(
      '/auth/token',
      new URLSearchParams({
        username,
        password,
      }),
      {
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
        },
      }
    );
    return response.data;
  },
};

export const tasksAPI = {
  list: async (completed?: boolean) => {
    const params = completed !== undefined ? { completed } : {};
    const response = await api.get<any>('/api/tasks', { params });
    // Backend returns {tasks: [...]} format
    return response.data.tasks || response.data;
  },

  get: async (id: number) => {
    const response = await api.get<Task>(`/api/tasks/${id}`);
    return response.data;
  },

  create: async (task: TaskCreate) => {
    const response = await api.post<Task>('/api/tasks', task);
    return response.data;
  },

  update: async (id: number, task: TaskUpdate) => {
    const response = await api.put<Task>(`/api/tasks/${id}`, task);
    return response.data;
  },

  delete: async (id: number) => {
    await api.delete(`/api/tasks/${id}`);
  },

  markComplete: async (id: number) => {
    const response = await api.patch<Task>(`/api/tasks/${id}/complete`);
    return response.data;
  },

  markIncomplete: async (id: number) => {
    const response = await api.patch<Task>(`/api/tasks/${id}/incomplete`);
    return response.data;
  },
};

export interface ChatMessage {
  role: 'user' | 'assistant';
  content: string;
}

export interface ChatRequest {
  message: string;
  conversation_history?: ChatMessage[];
}

export interface ChatResponse {
  message: string;
  conversation_id: string;
  conversation_history: ChatMessage[];
}

export interface MessageResponse {
  id: number;
  role: string;
  content: string;
  conversation_id: number;
  created_at: string;
}

export interface ConversationResponse {
  id: number;
  title?: string;
  owner_id: number;
  created_at: string;
  updated_at: string;
  messages: MessageResponse[];
}

export const chatAPI = {
  send: async (message: string, conversation_history?: ChatMessage[], conversation_id?: number | string) => {
    const response = await api.post<ChatResponse>('/api/chat', {
      message,
      conversation_history,
      conversation_id: conversation_id?.toString(),
    });
    return response.data;
  },

  getConversations: async () => {
    const response = await api.get<ConversationResponse[]>('/chat/conversations');
    return response.data;
  },

  getConversation: async (id: number) => {
    const response = await api.get<ConversationResponse>(`/chat/conversations/${id}`);
    return response.data;
  },

  deleteConversation: async (id: number) => {
    await api.delete(`/chat/conversations/${id}`);
  },
};
