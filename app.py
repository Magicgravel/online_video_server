import mimetypes
import os
from pathlib import Path
from typing import Iterable

from flask import Flask, Response, abort, render_template, request

VIDEO_EXTENSIONS = {
    ".ts",
    ".mp4",
    ".mkv",
    ".mov",
    ".webm",
    ".avi",
    ".m4v",
    ".mpg",
    ".mpeg",
}

BASE_DIR = Path("./videos").resolve()

app = Flask(__name__)


def iter_video_files(base_dir: Path) -> Iterable[str]:
    for path in base_dir.rglob("*"):
        if path.is_file() and path.suffix.lower() in VIDEO_EXTENSIONS:
            yield str(path.relative_to(base_dir))


def safe_resolve(base_dir: Path, relative_path: str) -> Path:
    resolved = (base_dir / relative_path).resolve()
    if not str(resolved).startswith(str(base_dir)):
        raise ValueError("Path escapes base directory")
    return resolved


@app.route("/")
def index() -> str:
    videos = sorted(iter_video_files(BASE_DIR))
    return render_template("index.html", videos=videos)


@app.route("/videos/<path:video_path>")
def serve_video(video_path: str) -> Response:
    try:
        full_path = safe_resolve(BASE_DIR, video_path)
    except ValueError:
        abort(404)

    if not full_path.exists() or not full_path.is_file():
        abort(404)

    file_size = full_path.stat().st_size
    range_header = request.headers.get("Range", "").strip()
    mimetype, _ = mimetypes.guess_type(str(full_path))
    mimetype = mimetype or "application/octet-stream"

    if range_header:
        bytes_unit, _, range_spec = range_header.partition("=")
        if bytes_unit != "bytes":
            abort(416)
        start_str, _, end_str = range_spec.partition("-")
        try:
            start = int(start_str) if start_str else 0
            end = int(end_str) if end_str else file_size - 1
        except ValueError:
            abort(416)
        start = max(0, start)
        end = min(end, file_size - 1)
        if start > end:
            abort(416)

        length = end - start + 1
        with open(full_path, "rb") as handle:
            handle.seek(start)
            data = handle.read(length)

        response = Response(data, 206, mimetype=mimetype, direct_passthrough=True)
        response.headers["Content-Range"] = f"bytes {start}-{end}/{file_size}"
        response.headers["Accept-Ranges"] = "bytes"
        response.headers["Content-Length"] = str(length)
        return response

    with open(full_path, "rb") as handle:
        data = handle.read()

    response = Response(data, 200, mimetype=mimetype, direct_passthrough=True)
    response.headers["Accept-Ranges"] = "bytes"
    response.headers["Content-Length"] = str(file_size)
    return response


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000, debug=True)
