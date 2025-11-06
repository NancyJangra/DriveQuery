"""
Documents API Routes
====================
Handles file uploads and document management
"""

from fastapi import APIRouter, UploadFile, File, HTTPException
from typing import List
import os
import shutil
from pydantic import BaseModel

from app.services.document_service import document_service

router = APIRouter()

class DocumentUploadResponse(BaseModel):
    """Response model for document upload"""
    doc_id: str
    filename: str
    pages: int = None
    chunks: int = 0
    total_chars: int

class DocumentListResponse(BaseModel):
    """Response model for document list"""
    documents: List[str]

@router.post("/documents/upload", response_model=DocumentUploadResponse)
async def upload_document(file: UploadFile = File(...)):
    """
    Upload a document (PDF, DOCX, or TXT)
    
    For beginners: This receives the file from the frontend,
    saves it, and processes it for searching.
    """
    
    # Check file extension
    filename = file.filename
    file_ext = os.path.splitext(filename)[1].lower()
    
    if file_ext not in ['.pdf', '.docx', '.txt']:
        raise HTTPException(
            status_code=400, 
            detail=f"Unsupported file type: {file_ext}. Please upload PDF, DOCX, or TXT files."
        )
    
    try:
        # Save uploaded file temporarily
        upload_path = os.path.join(document_service.upload_dir, filename)
        
        with open(upload_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Process the document
        result = document_service.process_document(upload_path, filename)
        
        return DocumentUploadResponse(**result)
        
    except Exception as e:
        # Clean up file if processing failed
        if os.path.exists(upload_path):
            os.remove(upload_path)
        
        raise HTTPException(
            status_code=500,
            detail=f"Failed to process document: {str(e)}"
        )

@router.get("/documents/list", response_model=DocumentListResponse)
async def list_documents():
    """
    Get list of all uploaded documents
    
    For beginners: Returns the names of all files that have been uploaded
    """
    try:
        documents = document_service.get_all_documents()
        return DocumentListResponse(documents=documents)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to list documents: {str(e)}"
        )

@router.delete("/documents/{filename}")
async def delete_document(filename: str):
    """
    Delete a specific document
    
    For beginners: Removes a file from the uploads folder
    """
    try:
        file_path = os.path.join(document_service.upload_dir, filename)
        
        if not os.path.exists(file_path):
            raise HTTPException(status_code=404, detail="Document not found")
        
        os.remove(file_path)
        
        return {"message": f"Document {filename} deleted successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to delete document: {str(e)}"
        )