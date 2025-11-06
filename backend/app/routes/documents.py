"""
Document Routes - API endpoints for document upload and management
Upload PDFs/DOCX and ask questions about them!
"""

from fastapi import APIRouter, UploadFile, File, HTTPException
from typing import List
from app.models.schemas import DocumentUploadResponse, DocumentInfo, ErrorResponse
from app.services.document_service import document_service

# Create router for document endpoints
router = APIRouter()

@router.post("/upload", response_model=DocumentUploadResponse)
async def upload_document(file: UploadFile = File(...)):
    """
    Upload a document (PDF or DOCX)
    
    The file will be processed and text will be extracted automatically.
    You'll get a file_id back that you can use to ask questions about the document.
    
    Args:
        file: The file to upload (PDF or DOCX)
        
    Returns:
        DocumentUploadResponse with file_id and status
    """
    try:
        # Validate file type
        allowed_types = ['.pdf', '.docx', '.doc']
        file_extension = file.filename.split('.')[-1].lower()
        
        if f'.{file_extension}' not in allowed_types:
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported file type. Allowed types: {', '.join(allowed_types)}"
            )
        
        print(f"📤 Uploading file: {file.filename}")
        
        # Read file content
        file_content = await file.read()
        
        # Process document
        result = document_service.process_document(
            file_content=file_content,
            filename=file.filename
        )
        
        if not result["success"]:
            raise HTTPException(
                status_code=400,
                detail=result.get("error", "Failed to process document")
            )
        
        print(f"✅ File uploaded successfully: {result['file_id']}")
        
        return DocumentUploadResponse(
            success=True,
            file_id=result["file_id"],
            filename=result["filename"],
            text_length=result["text_length"],
            message=result["message"]
        )
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Error uploading document: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error uploading document: {str(e)}"
        )

@router.get("/{file_id}", response_model=DocumentInfo)
async def get_document_info(file_id: str):
    """
    Get information about an uploaded document
    
    Args:
        file_id: The unique ID of the document
        
    Returns:
        DocumentInfo with details about the document
    """
    try:
        doc = document_service.get_document(file_id)
        
        if not doc:
            raise HTTPException(
                status_code=404,
                detail=f"Document with ID {file_id} not found"
            )
        
        return DocumentInfo(
            id=doc["id"],
            filename=doc["filename"],
            file_type=doc["file_type"],
            size=doc["size"],
            text_length=len(doc["text"])
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error retrieving document: {str(e)}"
        )

@router.get("/{file_id}/text")
async def get_document_text(file_id: str):
    """
    Get the extracted text from a document
    
    Args:
        file_id: The unique ID of the document
        
    Returns:
        The extracted text content
    """
    try:
        text = document_service.get_document_text(file_id)
        
        if not text:
            raise HTTPException(
                status_code=404,
                detail=f"Document with ID {file_id} not found"
            )
        
        return {
            "file_id": file_id,
            "text": text,
            "length": len(text)
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error retrieving document text: {str(e)}"
        )

@router.delete("/{file_id}")
async def delete_document(file_id: str):
    """
    Delete an uploaded document
    
    Args:
        file_id: The unique ID of the document to delete
        
    Returns:
        Success message
    """
    try:
        success = document_service.delete_document(file_id)
        
        if not success:
            raise HTTPException(
                status_code=404,
                detail=f"Document with ID {file_id} not found"
            )
        
        print(f"🗑️  Document deleted: {file_id}")
        
        return {
            "success": True,
            "message": "Document deleted successfully",
            "file_id": file_id
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error deleting document: {str(e)}"
        )

@router.get("/")
async def list_documents():
    """
    List all uploaded documents
    
    Returns:
        List of document IDs and filenames
    """
    try:
        from app.services.document_service import DOCUMENT_STORE
        
        documents = [
            {
                "id": doc["id"],
                "filename": doc["filename"],
                "file_type": doc["file_type"],
                "size": doc["size"]
            }
            for doc in DOCUMENT_STORE.values()
        ]
        
        return {
            "count": len(documents),
            "documents": documents
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error listing documents: {str(e)}"
        )
