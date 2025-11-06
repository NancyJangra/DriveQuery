/**
 * Type definitions for AutoQuery
 * These match the backend API models
 */

// ============= Chat Types =============

export interface ChatMessage {
  role: 'user' | 'assistant'
  content: string
  timestamp?: Date
}

export interface ChatRequest {
  message: string
  conversation_history?: ChatMessage[]
  document_id?: string | null
}

export interface ChatResponse {
  response: string
  conversation_id?: string | null
}

// ============= Document Types =============

export interface DocumentUploadResponse {
  success: boolean
  file_id?: string
  filename?: string
  text_length?: number
  message: string
  error?: string
}

export interface DocumentInfo {
  id: string
  filename: string
  file_type: string
  size: number
  text_length: number
}

export interface UploadedDocument {
  id: string
  filename: string
  uploadedAt: Date
  size: number
}

// ============= UI State Types =============

export interface AppState {
  messages: ChatMessage[]
  currentDocument: UploadedDocument | null
  isLoading: boolean
  error: string | null
}

// ============= Error Types =============

export interface ErrorResponse {
  error: string
  detail?: string
}
