import subprocess
from pathlib import Path

BASE_DIR = Path("../videos").resolve()


def convert_ts_to_mp4(base_dir: Path) -> None:
    if not base_dir.exists():
        raise FileNotFoundError(f"Videos directory not found: {base_dir}")

    for ts_path in base_dir.rglob("*.ts"):
        if not ts_path.is_file():
            continue

        mp4_path = ts_path.with_suffix(".mp4")
        if mp4_path.exists():
            print(f"Skip (exists): {mp4_path}")
            continue

        cmd = [
            "ffmpeg",
            "-y",
            "-i",
            str(ts_path),
            "-c",
            "copy",
            "-movflags",
            "+faststart",
            str(mp4_path),
        ]
        print(f"Converting: {ts_path} -> {mp4_path}")
        subprocess.run(cmd, check=True)


if __name__ == "__main__":
    convert_ts_to_mp4(BASE_DIR)
