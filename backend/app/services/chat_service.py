"""
Chat Service - Handles AI interactions with OpenAI GPT
This is where the magic happens! We talk to OpenAI here.
"""

import os
from openai import OpenAI
from typing import List, Dict, Optional

# Initialize OpenAI client
# This reads your API key from the .env file
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class ChatService:
    """
    Service class to handle all AI chat operations
    Think of this as your AI assistant manager
    """
    
    def __init__(self):
        """
        Initialize the chat service
        """
        self.model = "gpt-4"  # You can also use "gpt-3.5-turbo" for faster/cheaper responses
        self.max_tokens = 2000  # Maximum length of response
        self.temperature = 0.7  # Creativity (0 = deterministic, 1 = creative)
    
    async def get_chat_response(
        self, 
        message: str, 
        conversation_history: List[Dict[str, str]] = None,
        context: str = None
    ) -> str:
        """
        Get a response from the AI
        
        Args:
            message: The user's question/message
            conversation_history: Previous messages (for context)
            context: Additional context (like document content)
        
        Returns:
            AI's response as a string
        """
        try:
            # Build the messages array for OpenAI
            messages = []
            
            # System message - tells the AI how to behave
            system_message = """You are AutoQuery, a helpful AI assistant built for document Q&A. 
            You are friendly, professional, and provide accurate information. 
            When answering questions about documents, cite specific parts when possible.
            Keep responses concise but informative."""
            
            # If there's document context, add it to the system message
            if context:
                system_message += f"\n\nDocument Context:\n{context[:3000]}"  # Limit context size
            
            messages.append({"role": "system", "content": system_message})
            
            # Add conversation history if provided
            if conversation_history:
                for msg in conversation_history[-5:]:  # Keep last 5 messages for context
                    messages.append(msg)
            
            # Add current user message
            messages.append({"role": "user", "content": message})
            
            # Call OpenAI API
            # This is where we actually talk to GPT!
            response = client.chat.completions.create(
                model=self.model,
                messages=messages,
                max_tokens=self.max_tokens,
                temperature=self.temperature,
                stream=False  # Set to True if you want streaming responses
            )
            
            # Extract the AI's response
            ai_response = response.choices[0].message.content
            
            return ai_response
            
        except Exception as e:
            print(f"Error in chat service: {str(e)}")
            return f"Sorry, I encountered an error: {str(e)}"
    
    async def get_streaming_response(
        self,
        message: str,
        conversation_history: List[Dict[str, str]] = None,
        context: str = None
    ):
        """
        Get a streaming response from AI (word by word)
        This makes the UI look more interactive!
        
        Args:
            message: The user's question
            conversation_history: Previous messages
            context: Document context
            
        Yields:
            Chunks of the response as they come
        """
        try:
            # Build messages (same as above)
            messages = []
            
            system_message = """You are AutoQuery, a helpful AI assistant. 
            Provide clear, accurate, and concise responses."""
            
            if context:
                system_message += f"\n\nDocument Context:\n{context[:3000]}"
            
            messages.append({"role": "system", "content": system_message})
            
            if conversation_history:
                for msg in conversation_history[-5:]:
                    messages.append(msg)
            
            messages.append({"role": "user", "content": message})
            
            # Call OpenAI with streaming enabled
            response = client.chat.completions.create(
                model=self.model,
                messages=messages,
                max_tokens=self.max_tokens,
                temperature=self.temperature,
                stream=True  # Enable streaming!
            )
            
            # Yield chunks as they come
            for chunk in response:
                if chunk.choices[0].delta.content is not None:
                    yield chunk.choices[0].delta.content
                    
        except Exception as e:
            yield f"Error: {str(e)}"

# Create a singleton instance
# This means we only create one ChatService for the entire app
chat_service = ChatService()
