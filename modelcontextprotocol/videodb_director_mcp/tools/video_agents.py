"""Video-related agents for VideoDB Director."""

from typing import Optional, Dict, Any
from .base_agent import BaseDirectorAgent


class SummarizeVideoAgent(BaseDirectorAgent):
    """Agent for summarizing videos."""
    
    def summarize(self, collection_id: str, video_id: str, prompt: Optional[str] = None) -> str:
        """Generate a summary of a video.
        
        Args:
            collection_id: Collection ID containing the video
            video_id: Video ID to summarize
            prompt: Optional custom prompt to guide the summary
            
        Returns:
            Summary text
        """
        message = f"Summarize video {video_id} in collection {collection_id}"
        if prompt:
            message += f" with focus on: {prompt}"
            
        response = self._send_message("summarize_video", message)
        return self._extract_response_content(response)


class UploadAgent(BaseDirectorAgent):
    """Agent for uploading media to VideoDB."""
    
    def upload(self, source: str, media_type: str = "video", name: Optional[str] = None, 
               source_type: str = "url") -> Dict[str, Any]:
        """Upload media content to VideoDB.
        
        Args:
            source: URL or file path to upload
            media_type: Type of media (video, audio, image)
            name: Optional name for the uploaded file
            source_type: Either 'url' or 'file'
            
        Returns:
            Upload response with video/media ID
        """
        message = f"Upload {media_type} from {source_type}: {source}"
        if name:
            message += f" with name: {name}"
            
        response = self._send_message("upload", message)
        return response


class IndexAgent(BaseDirectorAgent):
    """Agent for indexing videos."""
    
    def index(self, video_id: str, index_type: str = "spoken_words", 
              collection_id: Optional[str] = None) -> Dict[str, Any]:
        """Index a video for search purposes.
        
        Args:
            video_id: Video ID to index
            index_type: Type of indexing (spoken_words or scene)
            collection_id: Optional collection ID
            
        Returns:
            Indexing response
        """
        message = f"Index video {video_id} for {index_type}"
        if collection_id:
            message += f" in collection {collection_id}"
            
        response = self._send_message("index", message)
        return response


class SearchAgent(BaseDirectorAgent):
    """Agent for searching videos."""
    
    def search(self, query: str, search_type: str = "semantic", 
               index_type: str = "spoken_word", collection_id: Optional[str] = None) -> Dict[str, Any]:
        """Search for content within videos.
        
        Args:
            query: Search query
            search_type: Type of search (semantic or keyword)
            index_type: Type of index to search (spoken_word or scene)
            collection_id: Optional collection ID to search within
            
        Returns:
            Search results
        """
        message = f"Search for '{query}' using {search_type} search on {index_type} index"
        if collection_id:
            message += f" in collection {collection_id}"
            
        response = self._send_message("search", message)
        return response


class PromptClipAgent(BaseDirectorAgent):
    """Agent for creating clips based on prompts."""
    
    def create_clips(self, prompt: str, video_id: str, collection_id: str,
                     content_type: str = "multimodal") -> Dict[str, Any]:
        """Create clips from a video based on prompts.
        
        Args:
            prompt: Prompt describing what to clip
            video_id: Video ID to create clips from
            collection_id: Collection ID
            content_type: Type of content (spoken_content, visual_content, multimodal)
            
        Returns:
            Created clips information
        """
        message = f"Create {content_type} clips from video {video_id} in collection {collection_id} based on: {prompt}"
        
        response = self._send_message("prompt_clip", message)
        return response


class FrameAgent(BaseDirectorAgent):
    """Agent for extracting frames from videos."""
    
    def extract_frame(self, video_id: str, collection_id: str, 
                      timestamp: Optional[float] = None) -> str:
        """Extract a frame from a video.
        
        Args:
            video_id: Video ID
            collection_id: Collection ID
            timestamp: Optional timestamp in seconds
            
        Returns:
            Frame URL or data
        """
        message = f"Extract frame from video {video_id} in collection {collection_id}"
        if timestamp:
            message += f" at timestamp {timestamp}s"
            
        response = self._send_message("frame", message)
        return self._extract_response_content(response)


class StreamVideoAgent(BaseDirectorAgent):
    """Agent for streaming videos."""
    
    def stream(self, video_id: str, collection_id: str) -> str:
        """Get streaming URL for a video.
        
        Args:
            video_id: Video ID
            collection_id: Collection ID
            
        Returns:
            Streaming URL
        """
        message = f"Stream video {video_id} from collection {collection_id}"
        
        response = self._send_message("stream_video", message)
        return self._extract_response_content(response)


class DownloadAgent(BaseDirectorAgent):
    """Agent for downloading videos."""
    
    def download(self, stream_link: str, name: Optional[str] = None) -> str:
        """Get download URL for a video.
        
        Args:
            stream_link: Stream link to download
            name: Optional name for the download
            
        Returns:
            Download URL
        """
        message = f"Download video from stream: {stream_link}"
        if name:
            message += f" with name: {name}"
            
        response = self._send_message("download", message)
        return self._extract_response_content(response)