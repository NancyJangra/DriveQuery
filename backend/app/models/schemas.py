"""
Data Models (Pydantic)
======================
These define the structure of data we send/receive.
Think of these as "types" for our API requests and responses.

Pydantic automatically validates data - super useful!
"""

from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

# ==================== CHAT MODELS ====================

class ChatMessage(BaseModel):
    """Single chat message"""
    role: str = Field(..., description="Either 'user' or 'assistant'")
    content: str = Field(..., description="The message text")
    timestamp: Optional[datetime] = None

class ChatRequest(BaseModel):
    """Request to send a chat message"""
    message: str = Field(..., description="User's question/message")
    session_id: Optional[str] = Field(None, description="Session ID for conversation history")
    use_documents: bool = Field(True, description="Whether to search uploaded documents")
    
    class Config:
        json_schema_extra = {
            "example": {
                "message": "What is the refund policy?",
                "session_id": "user123",
                "use_documents": True
            }
        }

class ChatResponse(BaseModel):
    """Response from chat endpoint"""
    message: str = Field(..., description="AI's response")
    sources: Optional[List[str]] = Field(None, description="Source documents used")
    session_id: str = Field(..., description="Session ID")
    
    class Config:
        json_schema_extra = {
            "example": {
                "message": "Based on the policy document, refunds are processed within 7 days...",
                "sources": ["policy.pdf"],
                "session_id": "user123"
            }
        }

# ==================== DOCUMENT MODELS ====================

class DocumentUploadResponse(BaseModel):
    """Response after uploading a document"""
    success: bool = Field(..., description="Whether upload was successful")
    filename: str = Field(..., description="Name of uploaded file")
    document_id: str = Field(..., description="Unique document ID")
    pages: Optional[int] = Field(None, description="Number of pages (for PDFs)")
    message: str = Field(..., description="Status message")
    
    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "filename": "employee_handbook.pdf",
                "document_id": "doc_123abc",
                "pages": 45,
                "message": "Document uploaded and processed successfully!"
            }
        }

class DocumentInfo(BaseModel):
    """Information about an uploaded document"""
    document_id: str
    filename: str
    upload_date: datetime
    size: int  # in bytes
    pages: Optional[int] = None
    status: str  # "processed", "processing", "failed"

class DocumentListResponse(BaseModel):
    """List of all uploaded documents"""
    documents: List[DocumentInfo]
    total: int

# ==================== ERROR MODELS ====================

class ErrorResponse(BaseModel):
    """Standard error response"""
    error: str = Field(..., description="Error message")
    detail: Optional[str] = Field(None, description="Detailed error info")
    
    class Config:
        json_schema_extra = {
            "example": {
                "error": "Invalid file format",
                "detail": "Only PDF, DOCX, and TXT files are supported"
            }
        }
