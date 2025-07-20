from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
import os
import json
import requests
import logging


class AIClient(ABC):
    """Abstract base class for AI clients."""
    
    @abstractmethod
    def generate_response(self, messages: List[Dict[str, str]]) -> str:
        """Generate a response from the AI model."""
        pass
    
    @abstractmethod
    def generate_judge_response(self, prompt: str) -> str:
        """Generate a judge response for competitive mode."""
        pass


class OpenAIClient(AIClient):
    """OpenAI API client for generating responses."""
    
    def __init__(self, api_key: str = None, model: str = "gpt-4o"):
        """Initialize with API key and model configuration."""
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.model = model
        self.base_url = "https://api.openai.com/v1/chat/completions"
        
        if not self.api_key:
            raise ValueError("OpenAI API key is required")
    
    def generate_response(self, messages: List[Dict[str, str]]) -> str:
        """Generate a character response using OpenAI API."""
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            }
            
            data = {
                "model": self.model,
                "messages": messages,
                "max_tokens": 100,  # Reduced to ensure ~50 word limit
                "temperature": 0.8,
                "presence_penalty": 0.1,
                "frequency_penalty": 0.1,
            }
            
            # Log the request for debugging
            logging.debug(f"[OpenAI REQUEST] Payload: {json.dumps(data, indent=2)}")
            
            # Make the request with explicit proxy disabling
            response = requests.post(
                self.base_url,
                headers=headers,
                json=data,
                timeout=30,
                proxies=None,  # Explicitly disable proxies
            )
            
            if response.status_code == 200:
                result = response.json()
                ai_response = result["choices"][0]["message"]["content"].strip()
                
                logging.debug(f"[OpenAI RESPONSE] Generated response: {ai_response}")
                return ai_response
            else:
                error_msg = f"HTTP {response.status_code} - {response.text}"
                logging.error(f"[OpenAI ERROR] {error_msg}")
                return f"Error: {error_msg}"
                
        except Exception as e:
            error_msg = f"Error generating response: {str(e)}"
            logging.error(f"[OpenAI ERROR] {error_msg}")
            return error_msg
    
    def generate_judge_response(self, prompt: str) -> str:
        """Generate a judge response for competitive mode."""
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            }
            
            data = {
                "model": self.model,
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": 300,
                "temperature": 0.3,
            }
            
            # Log the request for debugging
            logging.debug(f"[OpenAI JUDGE REQUEST] Payload: {json.dumps(data, indent=2)}")
            
            response = requests.post(
                self.base_url,
                headers=headers,
                json=data,
                timeout=30,
                proxies=None,
            )
            
            if response.status_code == 200:
                result = response.json()
                judge_response = result["choices"][0]["message"]["content"].strip()
                
                logging.debug(f"[OpenAI JUDGE RESPONSE] {judge_response}")
                return judge_response
            else:
                error_msg = f"HTTP {response.status_code} - {response.text}"
                logging.error(f"[OpenAI JUDGE ERROR] {error_msg}")
                return "{}"  # Return empty JSON for graceful failure
                
        except Exception as e:
            error_msg = f"Error generating judge response: {str(e)}"
            logging.error(f"[OpenAI JUDGE ERROR] {error_msg}")
            return "{}"  # Return empty JSON for graceful failure


class MockAIClient(AIClient):
    """Mock AI client for testing purposes."""
    
    def __init__(self, fixed_response: str = None, fixed_judge_response: str = None):
        """Initialize with optional fixed responses."""
        self.fixed_response = fixed_response
        self.fixed_judge_response = fixed_judge_response
        self.call_count = 0
        self.judge_call_count = 0
    
    def generate_response(self, messages: List[Dict[str, str]]) -> str:
        """Generate a mock response."""
        self.call_count += 1
        
        if self.fixed_response:
            return self.fixed_response
        
        # Generate a simple mock response based on the last message
        last_message = messages[-1]["content"] if messages else "Hello"
        
        # Extract character name from system message if available
        character_name = "Character"
        for msg in messages:
            if msg["role"] == "system" and "You are" in msg["content"]:
                # Try to extract character name
                try:
                    lines = msg["content"].split("\n")
                    for line in lines:
                        if line.strip().startswith("You are"):
                            character_name = line.split("You are")[1].split(",")[0].strip()
                            break
                except:
                    pass
                break
        
        return f"Mock response from {character_name} (call #{self.call_count}): {last_message[:20]}..."
    
    def generate_judge_response(self, prompt: str) -> str:
        """Generate a mock judge response."""
        self.judge_call_count += 1
        
        if self.fixed_judge_response:
            return self.fixed_judge_response
        
        # Return a simple mock judge response
        return '{"Character 1": {"anger": 1, "patience": 0, "uniqueness": 2}, "Character 2": {"anger": -1, "patience": 1, "uniqueness": 1}}'


class AIClientError(Exception):
    """Custom exception for AI client errors."""
    pass


def create_ai_client(client_type: str = "openai", **kwargs) -> AIClient:
    """Factory function to create AI clients."""
    if client_type == "openai":
        return OpenAIClient(
            api_key=kwargs.get("api_key"),
            model=kwargs.get("model", "gpt-4o")
        )
    elif client_type == "mock":
        return MockAIClient(
            fixed_response=kwargs.get("fixed_response"),
            fixed_judge_response=kwargs.get("fixed_judge_response")
        )
    else:
        raise ValueError(f"Unknown AI client type: {client_type}")


def validate_api_key(api_key: str) -> bool:
    """Validate if an API key is properly formatted."""
    if not api_key:
        return False
    
    # Basic validation for OpenAI API key format
    if api_key.startswith("sk-") and len(api_key) > 20:
        return True
    
    return False


def test_ai_connection(client: AIClient) -> bool:
    """Test if the AI client can make a successful connection."""
    try:
        test_messages = [
            {"role": "system", "content": "You are a test assistant."},
            {"role": "user", "content": "Say hello."}
        ]
        response = client.generate_response(test_messages)
        return len(response) > 0 and "error" not in response.lower()
    except Exception:
        return False