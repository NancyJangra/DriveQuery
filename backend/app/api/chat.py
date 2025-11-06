"""
Chat API Routes with OpenAI Integration
========================================
Handles chat/question answering functionality using OpenAI GPT
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import os
from openai import OpenAI

from app.services.document_service import document_service

router = APIRouter()

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class ChatRequest(BaseModel):
    """Request model for chat"""
    message: str

class ChatResponse(BaseModel):
    """Response model for chat"""
    response: str
    sources: Optional[List[str]] = []

@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    """
    Chat endpoint - Ask questions about uploaded documents using OpenAI
    
    This searches your documents and uses GPT to generate intelligent answers
    """
    
    if not request.message or not request.message.strip():
        raise HTTPException(status_code=400, detail="Message cannot be empty")
    
    try:
        # Search for relevant document chunks
        relevant_docs = document_service.search_documents(request.message, top_k=3)
        
        # Build context from documents
        if relevant_docs:
            context = "\n\n".join([f"Document Section {i+1}:\n{doc}" for i, doc in enumerate(relevant_docs)])
            sources = [f"Manual section {i+1}" for i in range(len(relevant_docs))]
        else:
            context = "No relevant information found in uploaded manuals."
            sources = []
        
        # Create the prompt for OpenAI - OPTIMIZED FOR SHORT ANSWERS
        system_prompt = """You are an expert automotive assistant specializing in vehicle manuals.

IMPORTANT RESPONSE RULES:
1. Keep answers SHORT and CONCISE (2-4 sentences max)
2. Use bullet points for steps or lists
3. Get straight to the point - no long explanations
4. If it's a procedure, list steps briefly with numbers
5. Only include essential information

Format your answers like this:
- For simple questions: Give a direct 1-2 sentence answer
- For procedures: Use numbered steps (keep each step to one line)
- For specifications: Give the exact number/value first, then brief context if needed"""

        user_prompt = f"""Question: {request.message}

Manual Information:
{context}

Give a SHORT, CONCISE answer. Maximum 3-4 sentences or use bullet points/numbered steps."""

        # Call OpenAI API
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.5,  # Lower temperature for more focused answers
            max_tokens=200    # Limit token count for shorter responses
        )
        
        # Extract the response
        ai_response = response.choices[0].message.content
        
        return ChatResponse(response=ai_response, sources=sources)
        
    except Exception as e:
        # Log the error
        print(f"Error in chat endpoint: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate response: {str(e)}"
        )

@router.get("/chat/history")
def get_chat_history():
    """
    Get chat history (if implemented)
    
    For beginners: This would return previous conversations
    Currently returns empty list
    """
    return {"history": []}