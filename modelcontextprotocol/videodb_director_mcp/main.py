import os
import threading
import time
import uuid
import requests
import argparse
import socketio
import webbrowser
from typing import Any, Optional, Dict, List
from mcp.server.fastmcp import FastMCP
from .cli_commands import (
    install_for_claude,
    install_for_cursor,
    install_for_all,
)
from .constants import (
    CODE_ASSISTANT_TXT_URL,
    DOCS_ASSISTANT_TXT_URL,
    DIRECTOR_CALL_DESCRIPTION,
    DIRECTOR_API,
)
from .tools import (
    # Video agents
    SummarizeVideoAgent,
    UploadAgent,
    IndexAgent,
    SearchAgent,
    PromptClipAgent,
    FrameAgent,
    StreamVideoAgent,
    DownloadAgent,
    # Processing agents
    SubtitleAgent,
    TranscriptionAgent,
    DubbingAgent,
    EditingAgent,
    CensorAgent,
    # Generation agents
    VideoGenerationAgent,
    AudioGenerationAgent,
    ImageGenerationAgent,
    # Utility agents
    MeetingRecorderAgent,
    WebSearchAgent,
    PricingAgent,
    CodeAssistantAgent
)


mcp = FastMCP("videodb-director")

# Keep existing resources
@mcp.resource(
    "videodb://doc_assistant",
    name="doc_assistant",
    description="Context for creating video applications using VideoDB",
)
def doc_assistant() -> str:
    try:
        response = requests.get(DOCS_ASSISTANT_TXT_URL)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        return f"Error: Unable to fetch data from URL. Details: {str(e)}"


@mcp.tool(
    name="doc_assistant",
    description="Context for creating video applications using VideoDB",
)
def doc_assistant() -> str:
    try:
        response = requests.get(DOCS_ASSISTANT_TXT_URL)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        return f"Error: Unable to fetch data from URL. Details: {str(e)}"


@mcp.resource(
    "videodb://code_assistant",
    name="code_assistant",
    description="Context for creating video applications using VideoDB",
)
def code_assistant() -> str:
    try:
        response = requests.get(CODE_ASSISTANT_TXT_URL)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        return f"Error: Unable to fetch data from URL. Details: {str(e)}"


@mcp.tool(
    name="code_assistant",
    description="Will give you data related to VideoDB SDK which allows developers to use videodb in python. IMPORTANT: Whenever user wants to write code related to videos, youtube videos or VideoDB specifically, always call this tool.",
)
def code_assistant() -> str:
    try:
        response = requests.get(CODE_ASSISTANT_TXT_URL)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        return f"Error: Unable to fetch data from URL. Details: {str(e)}"


@mcp.tool(
    name="play_video",
    description="Play the video of the given stream link",
)
async def play_video(stream_link: str) -> dict[str, Any]:
    webbrowser.open(f"https://console.videodb.io/player?url={stream_link}")
    return {"message": "Opening VideoDB in browser"}


# Keep the original call_director for backward compatibility
@mcp.tool(name="call_director", description=DIRECTOR_CALL_DESCRIPTION)
async def call_director(
    text_message: str, session_id: str | None = None, agents: list[str] = []
) -> dict[str, Any]:
    """
    Orchestrates specialized agents within the VideoDB server to efficiently handle multimedia and video-related queries.

    Args:
        text_message (str): The natural language query that Director will interpret and delegate to appropriate agents.
        session_id (str | None, optional): A session identifier to maintain continuity across multiple requests. If a previous response from this method included a `session_id`, it is MANDATORY to include it in subsequent requests.
    """
    api_key = os.getenv("VIDEODB_API_KEY")
    if not api_key:
        raise RuntimeError(
            "Missing VIDEODB_API_KEY environment variable. Please set it before calling this function."
        )
    url = DIRECTOR_API
    timeout = 300
    headers = {"x-access-token": api_key}
    sio = socketio.Client()
    response_data = None
    response_event = threading.Event()

    def on_connect():
        message = {
            "msg_type": "input",
            "sender": "user",
            "conv_id": str(int(time.time() * 1000)),
            "msg_id": str(int(time.time() * 1000) + 1),
            "session_id": session_id if session_id else str(uuid.uuid4()),
            "content": [{"type": "text", "text": text_message}],
            "agents": agents,
            "collection_id": "default",
        }
        sio.emit("chat", message, namespace="/chat")

    def on_message(data):
        nonlocal response_data
        if isinstance(data, dict) and data.get("status") != "progress":
            response_data = data
            response_event.set()

    sio.on("connect", on_connect, namespace="/chat")
    sio.on("chat", on_message, namespace="/chat")

    try:
        sio.connect(
            url,
            namespaces=["/", "/chat"],
            headers=headers,
            wait=True,
            wait_timeout=10,
            retry=True
        )
        received = response_event.wait(timeout=timeout)
    except Exception as e:
        return {"error": f"Connection failed :( : {e}"}
    finally:
        sio.disconnect()

    return response_data if received else {"error": "Timeout waiting for response"}


# Video Agent Tools
@mcp.tool(
    name="summarize_video",
    description="Generate a summary of a video using VideoDB"
)
async def summarize_video(collection_id: str, video_id: str, prompt: Optional[str] = None) -> str:
    agent = SummarizeVideoAgent()
    return agent.summarize(collection_id, video_id, prompt)


@mcp.tool(
    name="upload",
    description="Upload media content (video, audio, or image) to VideoDB"
)
async def upload(source: str, media_type: str = "video", name: Optional[str] = None, source_type: str = "url") -> Dict[str, Any]:
    agent = UploadAgent()
    return agent.upload(source, media_type, name, source_type)


@mcp.tool(
    name="index",
    description="Index a video for search purposes (spoken words or scenes)"
)
async def index(video_id: str, index_type: str = "spoken_words", collection_id: Optional[str] = None) -> Dict[str, Any]:
    agent = IndexAgent()
    return agent.index(video_id, index_type, collection_id)


@mcp.tool(
    name="search",
    description="Search for content within videos using semantic or keyword search"
)
async def search(query: str, search_type: str = "semantic", index_type: str = "spoken_word", collection_id: Optional[str] = None) -> Dict[str, Any]:
    agent = SearchAgent()
    return agent.search(query, search_type, index_type, collection_id)


@mcp.tool(
    name="prompt_clip",
    description="Create clips from a video based on prompts"
)
async def prompt_clip(prompt: str, video_id: str, collection_id: str, content_type: str = "multimodal") -> Dict[str, Any]:
    agent = PromptClipAgent()
    return agent.create_clips(prompt, video_id, collection_id, content_type)


@mcp.tool(
    name="frame",
    description="Extract a single frame from a video"
)
async def frame(video_id: str, collection_id: str, timestamp: Optional[float] = None) -> str:
    agent = FrameAgent()
    return agent.extract_frame(video_id, collection_id, timestamp)


@mcp.tool(
    name="stream_video",
    description="Get streaming URL for a video"
)
async def stream_video(video_id: str, collection_id: str) -> str:
    agent = StreamVideoAgent()
    return agent.stream(video_id, collection_id)


@mcp.tool(
    name="download",
    description="Get download URL for a video"
)
async def download(stream_link: str, name: Optional[str] = None) -> str:
    agent = DownloadAgent()
    return agent.download(stream_link, name)


# Processing Agent Tools
@mcp.tool(
    name="subtitle",
    description="Add subtitles to a video in a specified language"
)
async def subtitle(video_id: str, collection_id: str, language: str, style_notes: Optional[str] = None) -> Dict[str, Any]:
    agent = SubtitleAgent()
    return agent.add_subtitles(video_id, collection_id, language, style_notes)


@mcp.tool(
    name="transcription",
    description="Get transcription of a video"
)
async def transcription(video_id: str, collection_id: str, include_timestamps: bool = True, time_range: Optional[List[float]] = None) -> str:
    agent = TranscriptionAgent()
    range_tuple = tuple(time_range) if time_range else None
    return agent.transcribe(video_id, collection_id, include_timestamps, range_tuple)


@mcp.tool(
    name="dubbing",
    description="Dub a video into another language"
)
async def dubbing(video_id: str, collection_id: str, target_language: str, language_code: str, engine: Optional[str] = None) -> Dict[str, Any]:
    agent = DubbingAgent()
    return agent.dub(video_id, collection_id, target_language, language_code, engine)


@mcp.tool(
    name="editing",
    description="Edit or combine videos in a collection"
)
async def editing(collection_id: str, instructions: str) -> Dict[str, Any]:
    agent = EditingAgent()
    return agent.edit(collection_id, instructions)


@mcp.tool(
    name="censor",
    description="Censor profanities or specified content in a video"
)
async def censor(video_id: str, collection_id: str, custom_prompt: Optional[str] = None) -> Dict[str, Any]:
    agent = CensorAgent()
    return agent.censor(video_id, collection_id, custom_prompt)


# Generation Agent Tools
@mcp.tool(
    name="video_generation",
    description="Generate videos from text or images"
)
async def video_generation(collection_id: str, prompt: str, generation_type: str = "text_to_video", engine: Optional[str] = None, config: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    agent = VideoGenerationAgent()
    return agent.generate_video(collection_id, prompt, generation_type, engine, config)


@mcp.tool(
    name="audio_generation",
    description="Generate speech, sound effects, or music"
)
async def audio_generation(collection_id: str, text: str, job_type: str = "text_to_speech", engine: Optional[str] = None, config: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    agent = AudioGenerationAgent()
    return agent.generate_audio(collection_id, text, job_type, engine, config)


@mcp.tool(
    name="image_generation",
    description="Generate or enhance images"
)
async def image_generation(collection_id: str, prompt: str, generation_type: str = "text_to_image", config: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    agent = ImageGenerationAgent()
    return agent.generate_image(collection_id, prompt, generation_type, config)


# Utility Agent Tools
@mcp.tool(
    name="meeting_recorder",
    description="Record meetings from Google Meet or MS Teams"
)
async def meeting_recorder(meeting_url: str, title: Optional[str] = None, password: Optional[str] = None) -> Dict[str, Any]:
    agent = MeetingRecorderAgent()
    return agent.record_meeting(meeting_url, title, password)


@mcp.tool(
    name="web_search",
    description="Search for videos on the web"
)
async def web_search(query: str, num_results: int = 10, duration_filter: Optional[str] = None) -> List[Dict[str, Any]]:
    agent = WebSearchAgent()
    return agent.search_web(query, num_results, duration_filter)


@mcp.tool(
    name="pricing",
    description="Get pricing or usage information for VideoDB services"
)
async def pricing(query: str) -> str:
    agent = PricingAgent()
    return agent.get_pricing(query)


@mcp.tool(
    name="code_generator",
    description="Generate VideoDB-related code from natural language"
)
async def code_generator(prompt: str, language: str = "python") -> str:
    agent = CodeAssistantAgent()
    return agent.generate_code(prompt, language)


def parse_arguments():
    parser = argparse.ArgumentParser(description="Run the VideoDB MCP server.")
    parser.add_argument(
        "--api-key",
        type=str,
        help="🔑 The VideoDB API key required to connect to the VideoDB service.",
    )
    parser.add_argument(
        "--install",
        choices=["claude", "cursor", "all"],
        help="🔧 Configure the MCP server in 'claude' and/or 'cursor'.",
    )
    return parser.parse_args()


def main():
    args = parse_arguments()

    if args.install == "claude":
        install_for_claude()
        return

    if args.install == "cursor":
        install_for_cursor()
        return

    if args.install == "all":
        install_for_all()
        return

    if args.api_key:
        os.environ["VIDEODB_API_KEY"] = args.api_key

    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()