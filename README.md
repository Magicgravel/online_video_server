# Online Video Server

A lightweight Flask-based web application for streaming and browsing video files over HTTP. This server features built-in support for HTTP Range requests, enabling smooth video scrubbing and seeking in your web browser.

## Features

- **Video Streaming:** Supports HTTP 206 Partial Content, which allows seeking backwards and forwards while watching videos.
- **Multiple Formats:** Automatically detects and serves popular video formats including `.mp4`, `.mkv`, `.mov`, `.webm`, `.avi`, `.m4v`, `.mpg`, and `.mpeg`.
- **Directory Traversal Security:** Implements secure path resolution to prevent directory traversal attacks and ensures videos are only served from the authorized base directory.
- **Simple Web Interface:** Provides an easy-to-use web index to list and select videos for playback.

## Prerequisites

- Python 3.7 or higher

## Installation

1. Clone the repository or navigate to the project directory:
   ```bash
   cd online_video_server
   ```

2. (Optional but recommended) Create and activate a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Configuration

Before running the server, you need to configure the directory where your video files are stored. 

1. Open `app.py`.
2. Locate the `BASE_DIR` variable (around line 19):
   ```python
   BASE_DIR = Path("/home/u22/video_server/video").resolve()
   ```
3. Change the path to the absolute directory on your machine that contains your video files.

## Running the Server

Start the application by running:

```bash
python app.py
```

By default, the server will start on `http://0.0.0.0:3000/`. You can open this URL in your web browser to browse and play your video files.

*Note: The application currently runs in debug mode by default (`debug=True` in `app.py`). You may want to disable it for production use.*
