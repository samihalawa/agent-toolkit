"""Generation agents for creating videos, audio, and images."""

from typing import Optional, Dict, Any
from .base_agent import BaseDirectorAgent


class VideoGenerationAgent(BaseDirectorAgent):
    """Agent for generating videos from text or images."""
    
    def generate_video(self, collection_id: str, prompt: str, 
                       generation_type: str = "text_to_video",
                       engine: Optional[str] = None,
                       config: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Generate videos from text or images.
        
        Args:
            collection_id: Collection ID
            prompt: Text prompt or image reference
            generation_type: Either 'text_to_video' or 'image_to_video'
            engine: Optional generation engine (e.g., 'fal', 'stability')
            config: Optional configuration parameters
            
        Returns:
            Video generation response
        """
        message = f"Generate {generation_type} in collection {collection_id}: {prompt}"
        if engine:
            message += f" using {engine} engine"
        if config:
            message += f" with config: {config}"
            
        response = self._send_message("video_generation", message)
        return response


class AudioGenerationAgent(BaseDirectorAgent):
    """Agent for generating audio content."""
    
    def generate_audio(self, collection_id: str, text: str,
                       job_type: str = "text_to_speech",
                       engine: Optional[str] = None,
                       config: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Generate speech, sound effects, or music.
        
        Args:
            collection_id: Collection ID
            text: Text prompt or content
            job_type: Type of audio (text_to_speech, sound_effect, create_music)
            engine: Optional engine (e.g., 'elevenlabs', 'beatoven')
            config: Optional configuration
            
        Returns:
            Audio generation response
        """
        message = f"Generate {job_type} in collection {collection_id}: {text}"
        if engine:
            message += f" using {engine} engine"
        if config:
            message += f" with config: {config}"
            
        response = self._send_message("audio_generation", message)
        return response


class ImageGenerationAgent(BaseDirectorAgent):
    """Agent for generating or enhancing images."""
    
    def generate_image(self, collection_id: str, prompt: str,
                       generation_type: str = "text_to_image",
                       config: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Generate or enhance images.
        
        Args:
            collection_id: Collection ID
            prompt: Text prompt or image reference
            generation_type: Either 'text_to_image' or 'image_to_image'
            config: Optional configuration
            
        Returns:
            Image generation response
        """
        message = f"Generate {generation_type} in collection {collection_id}: {prompt}"
        if config:
            message += f" with config: {config}"
            
        response = self._send_message("image_generation", message)
        return response