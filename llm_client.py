"""LLM API client for communicating with Ollama or other LLM services."""

import requests
from typing import Optional, Dict, Any
import config


# System prompt for Byron Katie method
BYRON_KATIE_SYSTEM_PROMPT = """You are Lucy, a compassionate therapist trained in Byron Katie's "The Work" method. 
The Work consists of four questions and turnarounds to help examine stressful thoughts.

The four questions are:
1. Is it true?
2. Can you absolutely know that it's true?
3. How do you react—what happens—when you believe that thought?
4. Who would you be without the thought?

After the questions, you guide users through turnarounds - examining the thought from different perspectives.

Your responses should be:
- Compassionate and supportive
- Brief and focused on the current inquiry step
- In the style of "LUCY: [your response]"
- Guiding the user through self-inquiry rather than giving advice
"""


class LLMClient:
    """Client for interacting with LLM API endpoints."""
    
    def __init__(self, api_url: Optional[str] = None, model: Optional[str] = None, timeout: Optional[int] = None):
        """
        Initialize LLM client.
        
        Args:
            api_url: Base URL for the LLM API endpoint
            model: Model name to use (e.g., 'gemma2')
            timeout: Request timeout in seconds
        """
        self.api_url = api_url or config.LLM_API_URL
        self.model = model or config.LLM_MODEL
        self.timeout = timeout or config.LLM_TIMEOUT
        
    def is_available(self) -> bool:
        """Check if LLM API is configured and available."""
        return bool(self.api_url)
    
    def generate_response(self, prompt: str, context: Optional[str] = None) -> Dict[str, Any]:
        """
        Generate a response from the LLM.
        
        Args:
            prompt: The user's message or prompt
            context: Optional context for the conversation
            
        Returns:
            Dictionary with 'response' key containing the LLM's response
            or 'error' key if something went wrong
        """
        if not self.is_available():
            return {
                'error': 'LLM API URL is not configured',
                'fallback': True
            }
        
        try:
            # Prepare the request payload for Ollama API
            payload = {
                'model': self.model,
                'prompt': prompt,
                'stream': False
            }
            
            if context:
                payload['context'] = context
            
            # Make the API request
            response = requests.post(
                f"{self.api_url}/api/generate",
                json=payload,
                timeout=self.timeout
            )
            
            response.raise_for_status()
            data = response.json()
            
            return {
                'response': data.get('response', ''),
                'model': data.get('model', self.model),
                'context': data.get('context')
            }
            
        except requests.exceptions.Timeout:
            return {
                'error': 'LLM API request timed out',
                'fallback': True
            }
        except requests.exceptions.ConnectionError:
            return {
                'error': 'Could not connect to LLM API',
                'fallback': True
            }
        except requests.exceptions.HTTPError as e:
            return {
                'error': f'LLM API returned error: {e.response.status_code}',
                'fallback': True
            }
        except Exception as e:
            return {
                'error': f'Unexpected error: {str(e)}',
                'fallback': True
            }
    
    def generate_byron_katie_response(
        self, 
        user_statement: str, 
        conversation_step: int, 
        user_message_log: list
    ) -> Optional[str]:
        """
        Generate a Byron Katie method response using the LLM.
        
        Args:
            user_statement: The user's current message
            conversation_step: Current step in the conversation (0-based)
            user_message_log: List of previous user messages
            
        Returns:
            Generated response string or None if LLM should not be used
        """
        if not self.is_available():
            return None
        
        # Build context for the LLM
        prompt = self._build_byron_katie_context(user_statement, conversation_step, user_message_log)
        
        # Generate response
        result = self.generate_response(prompt)
        
        if 'error' in result:
            # Log error but return None to fall back to NLP mode
            print(f"LLM error: {result['error']}")
            return None
        
        return result.get('response')
    
    def _build_byron_katie_context(
        self, 
        user_statement: str, 
        conversation_step: int, 
        user_message_log: list
    ) -> str:
        """
        Build context prompt for Byron Katie method with the LLM.
        
        Args:
            user_statement: Current user statement
            conversation_step: Current conversation step
            user_message_log: Previous messages
            
        Returns:
            Formatted context string for the LLM
        """
        conversation_history = ""
        if user_message_log:
            conversation_history = "\n".join([f"User: {msg}" for msg in user_message_log])
        
        prompt = f"""{BYRON_KATIE_SYSTEM_PROMPT}

Conversation so far:
{conversation_history}

Current user message: {user_statement}
Current step: {conversation_step + 1}

Generate the appropriate Byron Katie method response for this step:"""
        
        return prompt
