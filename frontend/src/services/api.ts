/**
 * API Service
 * ===========
 * All API calls to the backend go through here.
 * Makes it easy to change endpoints or add error handling!
 * 
 * For beginners: These are just functions that make HTTP requests
 * using axios (like fetch but better!)
 */

import axios from 'axios';

// Create axios instance with base configuration
const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'https://drivequery-backend.onrender.com',
  headers: {
    'Content-Type': 'application/json',
  },
});

// Types for TypeScript
export interface ChatMessage {
  role: 'user' | 'assistant';
  content: string;
  timestamp?: string;
}

export interface ChatRequest {
  message: string;
  session_id?: string;
  use_documents?: boolean;
}

export interface ChatResponse {
  message: string;
  sources?: string[];
  session_id: string;
}

export interface DocumentUploadResponse {
  success: boolean;
  filename: string;
  document_id: string;
  pages?: number;
  message: string;
}

export interface DocumentInfo {
  document_id: string;
  filename: string;
  upload_date: string;
  size: number;
  pages?: number;
  status: string;
}

/**
 * Chat API
 * ========
 */
export const chatAPI = {
  /**
   * Send a chat message
   */
  sendMessage: async (request: ChatRequest): Promise<ChatResponse> => {
    const response = await api.post('/api/chat/message', request);
    return response.data;
  },

  /**
   * Send a message with streaming response
   * Returns an EventSource for Server-Sent Events
   */
  sendMessageStream: (request: ChatRequest) => {
    const params = new URLSearchParams({
      message: request.message,
      session_id: request.session_id || 'default',
      use_documents: String(request.use_documents ?? true),
    });

    const url = `${api.defaults.baseURL}/api/chat/message/stream?${params}`;
    return new EventSource(url);
  },

  /**
   * Clear chat session
   */
  clearSession: async (sessionId: string): Promise<void> => {
    await api.delete(`/api/chat/session/${sessionId}`);
  },

  /**
   * Get list of all sessions
   */
  listSessions: async (): Promise<any> => {
    const response = await api.get('/api/chat/sessions');
    return response.data;
  },
};

/**
 * Documents API
 * =============
 */
export const documentsAPI = {
  /**
   * Upload a document
   */
  upload: async (file: File): Promise<DocumentUploadResponse> => {
    const formData = new FormData();
    formData.append('file', file);

    const response = await api.post('/api/documents/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });

    return response.data;
  },

  /**
   * Get list of uploaded documents
   */
  list: async (): Promise<{ documents: DocumentInfo[]; total: number }> => {
    const response = await api.get('/api/documents/list');
    return response.data;
  },

  /**
   * Delete a document
   */
  delete: async (filename: string): Promise<void> => {
    await api.delete(`/api/documents/${filename}`);
  },

  /**
   * Search documents
   */
  search: async (query: string, topK: number = 5): Promise<any> => {
    const response = await api.get('/api/documents/search', {
      params: { query, top_k: topK },
    });
    return response.data;
  },

  /**
   * Get document stats
   */
  getStats: async (): Promise<any> => {
    const response = await api.get('/api/documents/stats');
    return response.data;
  },
};

/**
 * Error handler
 * =============
 */
api.interceptors.response.use(
  (response) => response,
  (error) => {
    // Handle errors globally
    if (error.response) {
      // Server responded with error status
      console.error('API Error:', error.response.data);
      throw new Error(error.response.data.detail || 'An error occurred');
    } else if (error.request) {
      // Request made but no response
      console.error('Network Error:', error.request);
      throw new Error('Network error. Please check your connection.');
    } else {
      // Something else happened
      console.error('Error:', error.message);
      throw error;
    }
  }
);
/**
 * Helper function for backward compatibility
 */
export const uploadDocument = async (file: File) => {
  try {
    const response = await documentsAPI.upload(file);
    return {
      success: true,
      file_id: response.document_id,
      filename: response.filename,
    };
  } catch (error: any) {
    return {
      success: false,
      error: error.message,
    };
  }
};

export default api;
