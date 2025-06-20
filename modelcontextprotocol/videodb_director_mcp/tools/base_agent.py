"""Base agent class for VideoDB Director agents."""

import os
import time
import json
from typing import Optional, Dict, Any, List
import socketio
from .exceptions import DirectorError


class BaseDirectorAgent:
    """Base class for all Director agents that communicate via VideoDB API."""
    
    def __init__(self):
        self.api_key = os.getenv("VIDEODB_API_KEY")
        if not self.api_key:
            raise DirectorError("VIDEODB_API_KEY environment variable is not set")
        
        self.base_url = "https://api2.director.videodb.io"
        self.namespace = "/chat"
        self.timeout = 300  # 5 minutes
        
    def _create_socket_client(self) -> socketio.Client:
        """Create and configure socket client."""
        sio = socketio.Client()
        return sio
        
    def _send_message(self, agent_name: str, message: str, session_id: Optional[str] = None) -> Dict[str, Any]:
        """Send message to specific Director agent and wait for response."""
        import threading
        import uuid
        
        sio = self._create_socket_client()
        response_data = None
        response_event = threading.Event()
        
        # Prepare message
        conv_id = str(int(time.time() * 1000))
        msg_id = str(int(time.time() * 1000) + 1)
        
        message_data = {
            "msg_type": "input",
            "sender": "user",
            "conv_id": conv_id,
            "msg_id": msg_id,
            "session_id": session_id if session_id else str(uuid.uuid4()),
            "content": [{"type": "text", "text": message}],
            "agents": [agent_name],
            "collection_id": "default"
        }
        
        def on_connect():
            sio.emit("chat", message_data, namespace=self.namespace)
        
        def on_chat(data):
            nonlocal response_data
            if isinstance(data, dict) and data.get("status") != "progress":
                response_data = data
                response_event.set()
        
        sio.on("connect", on_connect, namespace=self.namespace)
        sio.on("chat", on_chat, namespace=self.namespace)
        
        try:
            # Connect with proper headers
            sio.connect(
                self.base_url,
                namespaces=["/", self.namespace],
                headers={"x-access-token": self.api_key},
                wait=True,
                wait_timeout=10,
                retry=True
            )
            
            # Wait for response
            received = response_event.wait(timeout=self.timeout)
            
            if not received:
                raise DirectorError(f"Timeout waiting for response from {agent_name} agent")
                
            return response_data
            
        except Exception as e:
            raise DirectorError(f"Connection failed: {str(e)}")
        finally:
            try:
                sio.disconnect()
            except:
                pass
        
    def _extract_response_content(self, response: Dict[str, Any]) -> str:
        """Extract text content from agent response."""
        content = response.get("content", [])
        if content and isinstance(content[0], dict):
            return content[0].get("text", "")
        return str(content)