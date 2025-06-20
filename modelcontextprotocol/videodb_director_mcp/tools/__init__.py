"""Individual agents for direct access to VideoDB Director capabilities."""

from .video_agents import (
    SummarizeVideoAgent,
    UploadAgent,
    IndexAgent,
    SearchAgent,
    PromptClipAgent,
    FrameAgent,
    StreamVideoAgent,
    DownloadAgent
)
from .processing_agents import (
    SubtitleAgent,
    TranscriptionAgent,
    DubbingAgent,
    EditingAgent,
    CensorAgent
)
from .generation_agents import (
    VideoGenerationAgent,
    AudioGenerationAgent,
    ImageGenerationAgent
)
from .utility_agents import (
    MeetingRecorderAgent,
    WebSearchAgent,
    PricingAgent,
    CodeAssistantAgent
)

__all__ = [
    # Video agents
    "SummarizeVideoAgent",
    "UploadAgent",
    "IndexAgent",
    "SearchAgent",
    "PromptClipAgent",
    "FrameAgent",
    "StreamVideoAgent",
    "DownloadAgent",
    # Processing agents
    "SubtitleAgent",
    "TranscriptionAgent",
    "DubbingAgent",
    "EditingAgent",
    "CensorAgent",
    # Generation agents
    "VideoGenerationAgent",
    "AudioGenerationAgent",
    "ImageGenerationAgent",
    # Utility agents
    "MeetingRecorderAgent",
    "WebSearchAgent",
    "PricingAgent",
    "CodeAssistantAgent"
]