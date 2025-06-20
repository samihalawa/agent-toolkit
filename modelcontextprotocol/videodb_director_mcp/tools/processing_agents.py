"""Processing and editing agents for VideoDB Director."""

from typing import Optional, Dict, Any
from .base_agent import BaseDirectorAgent


class SubtitleAgent(BaseDirectorAgent):
    """Agent for adding subtitles to videos."""
    
    def add_subtitles(self, video_id: str, collection_id: str, language: str,
                      style_notes: Optional[str] = None) -> Dict[str, Any]:
        """Add subtitles to a video.
        
        Args:
            video_id: Video ID
            collection_id: Collection ID
            language: Target language for subtitles
            style_notes: Optional notes about subtitle style
            
        Returns:
            Subtitle generation response
        """
        message = f"Add {language} subtitles to video {video_id} in collection {collection_id}"
        if style_notes:
            message += f" with style: {style_notes}"
            
        response = self._send_message("subtitle", message)
        return response


class TranscriptionAgent(BaseDirectorAgent):
    """Agent for transcribing videos."""
    
    def transcribe(self, video_id: str, collection_id: str, 
                   include_timestamps: bool = True,
                   time_range: Optional[tuple] = None) -> str:
        """Get transcription of a video.
        
        Args:
            video_id: Video ID
            collection_id: Collection ID
            include_timestamps: Whether to include timestamps
            time_range: Optional (start, end) time range in seconds
            
        Returns:
            Transcription text
        """
        message = f"Transcribe video {video_id} in collection {collection_id}"
        if include_timestamps:
            message += " with timestamps"
        if time_range:
            message += f" from {time_range[0]}s to {time_range[1]}s"
            
        response = self._send_message("transcription", message)
        return self._extract_response_content(response)


class DubbingAgent(BaseDirectorAgent):
    """Agent for dubbing videos."""
    
    def dub(self, video_id: str, collection_id: str, target_language: str,
            language_code: str, engine: Optional[str] = None) -> Dict[str, Any]:
        """Dub a video into another language.
        
        Args:
            video_id: Video ID
            collection_id: Collection ID
            target_language: Target language name
            language_code: Target language code (e.g., 'fr', 'es')
            engine: Optional dubbing engine
            
        Returns:
            Dubbing response
        """
        message = f"Dub video {video_id} in collection {collection_id} to {target_language} ({language_code})"
        if engine:
            message += f" using {engine} engine"
            
        response = self._send_message("dubbing", message)
        return response


class EditingAgent(BaseDirectorAgent):
    """Agent for editing and combining videos."""
    
    def edit(self, collection_id: str, instructions: str) -> Dict[str, Any]:
        """Edit or combine videos in a collection.
        
        Args:
            collection_id: Collection ID containing videos to edit
            instructions: Editing instructions
            
        Returns:
            Editing response
        """
        message = f"Edit videos in collection {collection_id}: {instructions}"
        
        response = self._send_message("editing", message)
        return response


class CensorAgent(BaseDirectorAgent):
    """Agent for censoring content in videos."""
    
    def censor(self, video_id: str, collection_id: str, 
               custom_prompt: Optional[str] = None) -> Dict[str, Any]:
        """Censor profanities or specified content in a video.
        
        Args:
            video_id: Video ID
            collection_id: Collection ID
            custom_prompt: Optional custom censoring instructions
            
        Returns:
            Censoring response
        """
        message = f"Censor video {video_id} in collection {collection_id}"
        if custom_prompt:
            message += f" with custom rules: {custom_prompt}"
            
        response = self._send_message("censor", message)
        return response