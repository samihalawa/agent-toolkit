# Individual VideoDB Director Agents

This fork of the agent-toolkit now includes individual agents that provide direct access to specific VideoDB capabilities, instead of routing everything through the single `call_director` tool. All agents use the VideoDB API key for authentication.

## Video Agents

### summarize_video
Generate AI-powered summaries of videos.
- **Parameters:**
  - `collection_id` (str): Collection containing the video
  - `video_id` (str): Video to summarize
  - `prompt` (str, optional): Custom focus for the summary
- **Example:** `summarize_video("default", "video123", "Focus on key technical concepts")`

### upload
Upload media content to VideoDB.
- **Parameters:**
  - `source` (str): URL or file path
  - `media_type` (str): "video", "audio", or "image" (default: "video")
  - `name` (str, optional): Custom name for the upload
  - `source_type` (str): "url" or "file" (default: "url")
- **Example:** `upload("https://youtube.com/watch?v=...", "video", "Tutorial Video")`

### index
Index videos for search capabilities.
- **Parameters:**
  - `video_id` (str): Video to index
  - `index_type` (str): "spoken_words" or "scene" (default: "spoken_words")
  - `collection_id` (str, optional): Collection ID
- **Example:** `index("video123", "spoken_words")`

### search
Search within indexed videos.
- **Parameters:**
  - `query` (str): Search query
  - `search_type` (str): "semantic" or "keyword" (default: "semantic")
  - `index_type` (str): "spoken_word" or "scene" (default: "spoken_word")
  - `collection_id` (str, optional): Limit search to collection
- **Example:** `search("climate change", "semantic", "spoken_word")`

### prompt_clip
Create clips based on prompts.
- **Parameters:**
  - `prompt` (str): Description of desired clips
  - `video_id` (str): Source video
  - `collection_id` (str): Collection ID
  - `content_type` (str): "spoken_content", "visual_content", or "multimodal" (default: "multimodal")
- **Example:** `prompt_clip("moments discussing AI", "video123", "default")`

### frame
Extract frames from videos.
- **Parameters:**
  - `video_id` (str): Video ID
  - `collection_id` (str): Collection ID
  - `timestamp` (float, optional): Specific timestamp in seconds
- **Example:** `frame("video123", "default", 30.5)`

### stream_video
Get streaming URL for videos.
- **Parameters:**
  - `video_id` (str): Video to stream
  - `collection_id` (str): Collection ID
- **Example:** `stream_video("video123", "default")`

### download
Get download URL for processed content.
- **Parameters:**
  - `stream_link` (str): Stream link to download
  - `name` (str, optional): Custom download name
- **Example:** `download("https://stream.videodb.io/...")`

## Processing Agents

### subtitle
Add subtitles to videos.
- **Parameters:**
  - `video_id` (str): Video ID
  - `collection_id` (str): Collection ID
  - `language` (str): Target language (e.g., "Spanish", "French")
  - `style_notes` (str, optional): Subtitle style preferences
- **Example:** `subtitle("video123", "default", "Spanish")`

### transcription
Get video transcriptions.
- **Parameters:**
  - `video_id` (str): Video ID
  - `collection_id` (str): Collection ID
  - `include_timestamps` (bool): Include timestamps (default: True)
  - `time_range` (list[float], optional): [start, end] in seconds
- **Example:** `transcription("video123", "default", True, [0, 60])`

### dubbing
Dub videos into other languages.
- **Parameters:**
  - `video_id` (str): Video ID
  - `collection_id` (str): Collection ID
  - `target_language` (str): Target language name
  - `language_code` (str): Language code (e.g., "fr", "es")
  - `engine` (str, optional): Dubbing engine to use
- **Example:** `dubbing("video123", "default", "French", "fr")`

### editing
Edit and combine videos.
- **Parameters:**
  - `collection_id` (str): Collection with videos to edit
  - `instructions` (str): Editing instructions
- **Example:** `editing("default", "Combine intro.mp4 and main.mp4 with fade transition")`

### censor
Censor content in videos.
- **Parameters:**
  - `video_id` (str): Video ID
  - `collection_id` (str): Collection ID
  - `custom_prompt` (str, optional): Custom censoring rules
- **Example:** `censor("video123", "default", "Also censor brand names")`

## Generation Agents

### video_generation
Generate videos from text or images.
- **Parameters:**
  - `collection_id` (str): Collection ID
  - `prompt` (str): Generation prompt
  - `generation_type` (str): "text_to_video" or "image_to_video" (default: "text_to_video")
  - `engine` (str, optional): Generation engine (e.g., "fal", "stability")
  - `config` (dict, optional): Additional configuration
- **Example:** `video_generation("default", "serene beach sunset", "text_to_video", "stability")`

### audio_generation
Generate audio content.
- **Parameters:**
  - `collection_id` (str): Collection ID
  - `text` (str): Text or prompt
  - `job_type` (str): "text_to_speech", "sound_effect", or "create_music" (default: "text_to_speech")
  - `engine` (str, optional): Engine (e.g., "elevenlabs", "beatoven")
  - `config` (dict, optional): Additional configuration
- **Example:** `audio_generation("default", "Welcome to our channel", "text_to_speech", "elevenlabs")`

### image_generation
Generate or enhance images.
- **Parameters:**
  - `collection_id` (str): Collection ID
  - `prompt` (str): Generation prompt
  - `generation_type` (str): "text_to_image" or "image_to_image" (default: "text_to_image")
  - `config` (dict, optional): Additional configuration
- **Example:** `image_generation("default", "futuristic city skyline", "text_to_image")`

## Utility Agents

### meeting_recorder
Record online meetings.
- **Parameters:**
  - `meeting_url` (str): Meeting URL (Google Meet or MS Teams)
  - `title` (str, optional): Meeting title
  - `password` (str, optional): Meeting password if required
- **Example:** `meeting_recorder("https://meet.google.com/xyz", "Team Standup")`

### web_search
Search for videos on the web.
- **Parameters:**
  - `query` (str): Search query
  - `num_results` (int): Number of results (default: 10)
  - `duration_filter` (str, optional): "short", "medium", or "long"
- **Example:** `web_search("machine learning tutorials", 5, "medium")`

### pricing
Get VideoDB pricing information.
- **Parameters:**
  - `query` (str): Pricing query
- **Example:** `pricing("cost of processing 100 hours of video")`

### code_generator
Generate VideoDB SDK code.
- **Parameters:**
  - `prompt` (str): Natural language description
  - `language` (str): Programming language (default: "python")
- **Example:** `code_generator("upload a video and create subtitles", "python")`

## Implementation Details

All agents:
- Use the VideoDB API key from `VIDEODB_API_KEY` environment variable
- Communicate with the Director backend via WebSocket
- Return structured responses or error messages
- Support both synchronous and asynchronous operations

The original `call_director` tool remains available for backward compatibility and complex multi-agent workflows.