#!/usr/bin/env python3
"""Turn a photo's Instagram Story typography graphic into a short video with
background music, so it holds on screen longer than Instagram's default
~5s for a static photo Story (video Stories can run up to ~15s per segment).

Music source: assets/audio/dunya-bozorgtar-theme.mp3 (committed — Bahman
provided this track specifically for the series, 2026-08-12). A **random**
start offset is picked inside the track on every run (standing rule,
2026-08-12 — Bahman doesn't want every video opening on the same few
seconds of the song), long enough before the track's end to fit the full
clip duration.

ffmpeg: loop the still story image for DURATION seconds, mix in the audio
segment with a short fade-in/fade-out, output an H.264/AAC MP4 sized to
match the story image (1088x1920), faststart for web playback. Saved next
to the source image at images/ig-queue/stories/<asset_id>.mp4 — the .jpg
stays as the source design frame; the .mp4 is what actually gets posted as
an Instagram Story (via video_url, same as publish_story.py's pattern).

Usage:
    scripts/.venv/bin/python scripts/make_story_video.py <asset_id>
    scripts/.venv/bin/python scripts/make_story_video.py <asset_id> --duration 13
"""

import argparse
import random
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
STORIES_DIR = REPO_ROOT / "images" / "ig-queue" / "stories"
MUSIC_PATH = REPO_ROOT / "assets" / "audio" / "dunya-bozorgtar-theme.mp3"

DEFAULT_DURATION = 12.0  # seconds — within Bahman's "10-15s" target range
FADE_SECONDS = 1.0


def _music_duration(path: Path) -> float:
    result = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=noprint_wrappers=1:nokey=1", str(path)],
        capture_output=True, text=True, check=True,
    )
    return float(result.stdout.strip())


def make_video(asset_id: str, duration: float = DEFAULT_DURATION) -> Path:
    image_path = STORIES_DIR / f"{asset_id}.jpg"
    if not image_path.exists():
        raise SystemExit(f"No story image at {image_path} — run gpt_story_typography.py first")
    if not MUSIC_PATH.exists():
        raise SystemExit(f"No music track at {MUSIC_PATH}")

    track_len = _music_duration(MUSIC_PATH)
    if track_len <= duration:
        start = 0.0
    else:
        start = random.uniform(0, track_len - duration)

    out_path = STORIES_DIR / f"{asset_id}.mp4"
    fade_out_at = max(0.0, duration - FADE_SECONDS)

    cmd = [
        "ffmpeg", "-y",
        "-loop", "1", "-i", str(image_path),
        "-ss", f"{start:.2f}", "-t", f"{duration:.2f}", "-i", str(MUSIC_PATH),
        "-filter_complex",
        f"[1:a]afade=t=in:st=0:d={FADE_SECONDS},afade=t=out:st={fade_out_at:.2f}:d={FADE_SECONDS}[a]",
        "-map", "0:v", "-map", "[a]",
        "-t", f"{duration:.2f}",
        "-c:v", "libx264", "-pix_fmt", "yuv420p", "-vf", "scale=1088:1920",
        "-c:a", "aac", "-b:a", "128k",
        "-movflags", "+faststart",
        str(out_path),
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise SystemExit(f"ffmpeg failed:\n{result.stderr[-2000:]}")
    return out_path


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("asset_id")
    parser.add_argument("--duration", type=float, default=DEFAULT_DURATION)
    args = parser.parse_args()

    out_path = make_video(args.asset_id, args.duration)
    print(f"Saved: {out_path.relative_to(REPO_ROOT)} ({out_path.stat().st_size // 1024} KB)")


if __name__ == "__main__":
    main()
