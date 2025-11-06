"""
LLM Service - OpenAI Integration
=================================
This is where the "AI magic" happens! But it's actually super simple.
We just call OpenAI's API and they do all the hard work.

For beginners: You don't need to understand HOW GPT works internally.
Just know: Send text → Get smart response back!
"""

from openai import OpenAI
from app.core.config import settings
from typing import List, Optional
import logging

# Set up logging (helps with debugging)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LLMService:
    """
    Service to interact with OpenAI's GPT models
    This is the "AI brain" of your chatbot!
    """
    
    def __init__(self):
        """Initialize OpenAI client with API key"""
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
        self.model = settings.MODEL_NAME
        logger.info(f"LLM Service initialized with model: {self.model}")
    
    def chat(
        self, 
        user_message: str, 
        context: Optional[str] = None,
        conversation_history: Optional[List[dict]] = None
    ) -> str:
        """
        Send a message to GPT and get a response
        
        Args:
            user_message: The user's question/message
            context: Additional context (like document text)
            conversation_history: Previous messages in the conversation
        
        Returns:
            AI's response as a string
        """
        
        # Build the messages list for OpenAI
        messages = []
        
        # System message - tells GPT how to behave
        system_prompt = """You are AutoQuery, an intelligent AI assistant designed to help employees 
        find information quickly and accurately. You are helpful, professional, and concise.
        
        When answering questions:
        - Be clear and direct
        - If you don't know something, say so
        - If context is provided, base your answer on that context
        - Be friendly and professional
        """
        
        messages.append({"role": "system", "content": system_prompt})
        
        # Add conversation history if available
        if conversation_history:
            messages.extend(conversation_history)
        
        # Add context from documents if available
        if context:
            context_message = f"""Here is relevant information from the uploaded documents:

{context}

Please answer the user's question based on this information. If the answer is not in the documents, 
let the user know."""
            messages.append({"role": "system", "content": context_message})
        
        # Add the user's current message
        messages.append({"role": "user", "content": user_message})
        
        try:
            # Call OpenAI API - THIS IS WHERE THE MAGIC HAPPENS!
            # But really, it's just an API call. OpenAI does all the hard work.
            logger.info(f"Sending request to OpenAI with {len(messages)} messages")
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.7,  # Controls randomness (0=deterministic, 1=creative)
                max_tokens=1000,  # Maximum length of response
            )
            
            # Extract the response text
            ai_response = response.choices[0].message.content
            logger.info(f"Received response from OpenAI ({len(ai_response)} chars)")
            
            return ai_response
            
        except Exception as e:
            logger.error(f"Error calling OpenAI API: {str(e)}")
            raise Exception(f"Failed to get AI response: {str(e)}")
    
    def chat_stream(
        self, 
        user_message: str, 
        context: Optional[str] = None
    ):
        """
        Stream responses from GPT (for real-time typing effect)
        This makes your chatbot look more professional!
        
        Returns: Generator that yields response chunks
        """
        
        messages = [
            {"role": "system", "content": "You are a helpful AI assistant."},
        ]
        
        if context:
            messages.append({
                "role": "system", 
                "content": f"Context: {context}"
            })
        
        messages.append({"role": "user", "content": user_message})
        
        try:
            # Stream the response
            stream = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.7,
                max_tokens=1000,
                stream=True  # Enable streaming!
            )
            
            for chunk in stream:
                if chunk.choices[0].delta.content:
                    yield chunk.choices[0].delta.content
                    
        except Exception as e:
            logger.error(f"Error streaming from OpenAI: {str(e)}")
            yield f"Error: {str(e)}"

# Create a singleton instance
llm_service = LLMService()
