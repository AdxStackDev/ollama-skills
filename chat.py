#!/usr/bin/env python3
"""
Ollama Qwen2.5-Coder Application
Uses the qwen2.5-coder:7b model for code generation and assistance
"""

import requests
import json
from typing import Optional, Generator


class OllamaClient:
    """Client for interacting with Ollama API"""
    
    def __init__(self, base_url: str = "http://localhost:11434"):
        self.base_url = base_url
        self.model = "qwen2.5-coder:7b"
    
    def generate(self, prompt: str, stream: bool = True) -> Generator[str, None, None] | str:
        """
        Generate a response from the model
        
        Args:
            prompt: The input prompt
            stream: Whether to stream the response
            
        Yields:
            Response chunks if streaming, otherwise returns complete response
        """
        url = f"{self.base_url}/api/generate"
        data = {
            "model": self.model,
            "prompt": prompt,
            "stream": stream
        }
        
        try:
            response = requests.post(url, json=data, stream=stream)
            response.raise_for_status()
            
            if stream:
                for line in response.iter_lines():
                    if line:
                        chunk = json.loads(line)
                        if "response" in chunk:
                            yield chunk["response"]
                        if chunk.get("done", False):
                            break
            else:
                result = response.json()
                return result.get("response", "")
                
        except requests.exceptions.RequestException as e:
            print(f"Error communicating with Ollama: {e}")
            return "" if not stream else iter([])
    
    def chat(self, messages: list[dict], stream: bool = True) -> Generator[str, None, None] | str:
        """
        Chat with the model using conversation history
        
        Args:
            messages: List of message dicts with 'role' and 'content'
            stream: Whether to stream the response
            
        Yields:
            Response chunks if streaming, otherwise returns complete response
        """
        url = f"{self.base_url}/api/chat"
        data = {
            "model": self.model,
            "messages": messages,
            "stream": stream
        }
        
        try:
            response = requests.post(url, json=data, stream=stream)
            response.raise_for_status()
            
            if stream:
                for line in response.iter_lines():
                    if line:
                        chunk = json.loads(line)
                        if "message" in chunk and "content" in chunk["message"]:
                            yield chunk["message"]["content"]
                        if chunk.get("done", False):
                            break
            else:
                result = response.json()
                return result.get("message", {}).get("content", "")
                
        except requests.exceptions.RequestException as e:
            print(f"Error communicating with Ollama: {e}")
            return "" if not stream else iter([])
    
    def list_models(self) -> list[dict]:
        """List all available models"""
        url = f"{self.base_url}/api/tags"
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.json().get("models", [])
        except requests.exceptions.RequestException as e:
            print(f"Error listing models: {e}")
            return []


def main():
    """Main application entry point"""
    client = OllamaClient()
    
    print("=" * 60)
    print("Ollama Qwen2.5-Coder:7b Chat Interface")
    print("=" * 60)
    print("Type 'quit' or 'exit' to end the conversation")
    print("Type 'clear' to start a new conversation")
    print("=" * 60)
    print()
    
    # Verify the model is available
    models = client.list_models()
    if not any(m.get("name") == "qwen2.5-coder:7b" for m in models):
        print("Warning: qwen2.5-coder:7b model not found!")
        print("Available models:")
        for model in models:
            print(f"  - {model.get('name')}")
        print()
    
    # Conversation history
    messages = []
    
    while True:
        try:
            # Get user input
            user_input = input("\nYou: ").strip()
            
            if not user_input:
                continue
            
            if user_input.lower() in ['quit', 'exit']:
                print("\nGoodbye!")
                break
            
            if user_input.lower() == 'clear':
                messages = []
                print("\nConversation cleared!")
                continue
            
            # Add user message to history
            messages.append({
                "role": "user",
                "content": user_input
            })
            
            # Get response from model
            print("\nAssistant: ", end="", flush=True)
            full_response = ""
            
            for chunk in client.chat(messages, stream=True):
                print(chunk, end="", flush=True)
                full_response += chunk
            
            print()  # New line after response
            
            # Add assistant response to history
            messages.append({
                "role": "assistant",
                "content": full_response
            })
            
        except KeyboardInterrupt:
            print("\n\nInterrupted. Goodbye!")
            break
        except Exception as e:
            print(f"\nError: {e}")


if __name__ == "__main__":
    main()
