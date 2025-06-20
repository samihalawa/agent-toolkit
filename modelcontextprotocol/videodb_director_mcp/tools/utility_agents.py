"""Utility agents for various VideoDB operations."""

from typing import Optional, Dict, Any, List
from .base_agent import BaseDirectorAgent


class MeetingRecorderAgent(BaseDirectorAgent):
    """Agent for recording meetings."""
    
    def record_meeting(self, meeting_url: str, title: Optional[str] = None,
                       password: Optional[str] = None) -> Dict[str, Any]:
        """Record a meeting from Google Meet or MS Teams.
        
        Args:
            meeting_url: Meeting URL
            title: Optional meeting title
            password: Optional meeting password
            
        Returns:
            Recording response
        """
        message = f"Record meeting from {meeting_url}"
        if title:
            message += f" titled: {title}"
        if password:
            message += " (password provided)"
            
        response = self._send_message("meeting_recorder", message)
        return response


class WebSearchAgent(BaseDirectorAgent):
    """Agent for searching videos on the web."""
    
    def search_web(self, query: str, num_results: int = 10,
                   duration_filter: Optional[str] = None) -> List[Dict[str, Any]]:
        """Search for videos on the web.
        
        Args:
            query: Search query
            num_results: Number of results to return
            duration_filter: Optional duration filter (e.g., 'short', 'medium', 'long')
            
        Returns:
            List of search results
        """
        message = f"Search web for '{query}' (limit: {num_results})"
        if duration_filter:
            message += f" with duration: {duration_filter}"
            
        response = self._send_message("web_search", message)
        return response


class PricingAgent(BaseDirectorAgent):
    """Agent for pricing and usage information."""
    
    def get_pricing(self, query: str) -> str:
        """Get pricing or usage information.
        
        Args:
            query: Specific pricing query
            
        Returns:
            Pricing information
        """
        message = f"Pricing query: {query}"
        
        response = self._send_message("pricing", message)
        return self._extract_response_content(response)


class CodeAssistantAgent(BaseDirectorAgent):
    """Agent for generating VideoDB code."""
    
    def generate_code(self, prompt: str, language: str = "python") -> str:
        """Generate VideoDB-related code from natural language.
        
        Args:
            prompt: Natural language description of what to code
            language: Programming language (default: python)
            
        Returns:
            Generated code
        """
        message = f"Generate {language} code for: {prompt}"
        
        response = self._send_message("code_assistant", message)
        return self._extract_response_content(response)