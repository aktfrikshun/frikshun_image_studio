from __future__ import annotations

import argparse
import subprocess
import tempfile
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser(description="Stitch MP4 clips with simple ffmpeg concat.")
    parser.add_argument("--out", type=Path, required=True, help="Output MP4 path.")
    parser.add_argument("clips", type=Path, nargs="+", help="Input MP4 clips in order.")
    args = parser.parse_args()

    missing = [clip for clip in args.clips if not clip.exists()]
    if missing:
        raise SystemExit("Missing clips: " + ", ".join(str(path) for path in missing))

    args.out.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile("w", encoding="utf-8", suffix=".txt", delete=False) as manifest:
        manifest_path = Path(manifest.name)
        for clip in args.clips:
            escaped = str(clip.resolve()).replace("'", "'\\''")
            manifest.write(f"file '{escaped}'\n")

    try:
        command = [
            "ffmpeg",
            "-y",
            "-f",
            "concat",
            "-safe",
            "0",
            "-i",
            str(manifest_path),
            "-c",
            "copy",
            str(args.out),
        ]
        subprocess.run(command, check=True)
    finally:
        manifest_path.unlink(missing_ok=True)

    print(args.out)


if __name__ == "__main__":
    main()
