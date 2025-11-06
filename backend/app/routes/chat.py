"""
Chat Routes - API endpoints for chat functionality
These are the URLs the frontend calls to chat with the AI
"""

from fastapi import APIRouter, HTTPException
from app.models.schemas import ChatRequest, ChatResponse, ErrorResponse
from app.services.chat_service import chat_service
from app.services.document_service import document_service

# Create router for chat endpoints
router = APIRouter()

@router.post("/", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Main chat endpoint
    
    Send a message and get an AI response!
    
    Args:
        request: ChatRequest containing user message and optional context
        
    Returns:
        ChatResponse with AI's answer
    """
    try:
        # Get document context if document_id is provided
        context = None
        if request.document_id:
            # Fetch the document text
            context = document_service.get_document_text(request.document_id)
            
            if not context:
                raise HTTPException(
                    status_code=404,
                    detail=f"Document with ID {request.document_id} not found"
                )
            
            print(f"📄 Using document context ({len(context)} characters)")
        
        # Convert conversation history to the format OpenAI expects
        history = []
        if request.conversation_history:
            history = [
                {"role": msg.role, "content": msg.content}
                for msg in request.conversation_history
            ]
        
        # Get AI response
        print(f"💬 User: {request.message}")
        
        response_text = await chat_service.get_chat_response(
            message=request.message,
            conversation_history=history,
            context=context
        )
        
        print(f"🤖 AI: {response_text[:100]}...")
        
        return ChatResponse(
            response=response_text,
            conversation_id=None  # You can implement conversation tracking here
        )
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Error in chat endpoint: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error processing chat: {str(e)}"
        )

@router.post("/stream")
async def chat_stream(request: ChatRequest):
    """
    Streaming chat endpoint (optional advanced feature)
    
    Get AI responses word-by-word in real-time!
    This makes the UI feel more responsive.
    
    Note: Implementation would require Server-Sent Events (SSE)
    or WebSockets. For simplicity, we're using regular responses.
    """
    # TODO: Implement streaming with SSE or WebSockets
    # For now, just redirect to regular chat
    return await chat(request)

@router.get("/test")
async def test_chat():
    """
    Test endpoint to check if chat service is working
    
    Returns:
        A test message from the AI
    """
    try:
        response = await chat_service.get_chat_response(
            message="Say 'Hello! The chat service is working!' in a friendly way.",
            conversation_history=[],
            context=None
        )
        
        return {
            "status": "success",
            "message": "Chat service is operational",
            "test_response": response
        }
        
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }
