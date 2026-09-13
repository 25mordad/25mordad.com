#!/usr/bin/env python3
"""Transcribe Bahman's saved voice notes into Persian text for the voice-profile corpus.

Usage:
    scripts/.venv/bin/python scripts/transcribe_voice.py            # every file in files/voice/corpus/voice/
    scripts/.venv/bin/python scripts/transcribe_voice.py path/to/one.ogg

Input:  files/voice/corpus/voice/*.{ogg,m4a,mp3,wav,opus,aac,mp4}
Output: files/voice/corpus/voice/transcripts/<name>.txt  (skipped if it already exists)

Each file is converted with ffmpeg to 16 kHz mono MP3 and split into 10-minute chunks so no
upload exceeds OpenAI's 25 MB limit, then sent to the transcription endpoint with
language="fa". Uses OPENAI_API_KEY from the project-root .env (never printed).
The whole corpus folder is gitignored — nothing here is ever committed.
"""
from __future__ import annotations

import os
import subprocess
import sys
import tempfile
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

REPO_ROOT = Path(__file__).resolve().parent.parent
VOICE_DIR = REPO_ROOT / "files" / "voice" / "corpus" / "voice"
OUT_DIR = VOICE_DIR / "transcripts"
AUDIO_EXT = {".ogg", ".oga", ".opus", ".m4a", ".mp3", ".wav", ".aac", ".mp4", ".webm"}
MODEL = "gpt-4o-transcribe"
CHUNK_SECONDS = 600


def split_to_chunks(src: Path, tmp: Path) -> list[Path]:
    pattern = tmp / (src.stem + ".%03d.mp3")
    subprocess.run(
        [
            "ffmpeg", "-loglevel", "error", "-y", "-i", str(src),
            "-ac", "1", "-ar", "16000", "-b:a", "48k",
            "-f", "segment", "-segment_time", str(CHUNK_SECONDS),
            str(pattern),
        ],
        check=True,
    )
    return sorted(tmp.glob(src.stem + ".*.mp3"))


def transcribe(client: OpenAI, src: Path) -> str:
    with tempfile.TemporaryDirectory() as td:
        parts = []
        for chunk in split_to_chunks(src, Path(td)):
            with chunk.open("rb") as fh:
                res = client.audio.transcriptions.create(
                    model=MODEL, file=fh, language="fa", response_format="text"
                )
            parts.append(res.strip() if isinstance(res, str) else res.text.strip())
        return "\n\n".join(p for p in parts if p)


def main(argv: list[str]) -> int:
    load_dotenv(REPO_ROOT / ".env")
    if not os.environ.get("OPENAI_API_KEY"):
        print("OPENAI_API_KEY missing in .env", file=sys.stderr)
        return 1
    client = OpenAI()
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    if argv:
        files = [Path(a).resolve() for a in argv]
    else:
        files = sorted(p for p in VOICE_DIR.iterdir() if p.suffix.lower() in AUDIO_EXT)
    if not files:
        print(f"no audio files in {VOICE_DIR}")
        return 0

    for src in files:
        out = OUT_DIR / (src.stem + ".txt")
        if out.exists():
            print(f"skip  {src.name} (transcript exists)")
            continue
        print(f"trans {src.name} ...", flush=True)
        try:
            text = transcribe(client, src)
        except Exception as exc:  # noqa: BLE001 — report and keep going
            print(f"FAIL  {src.name}: {exc}", file=sys.stderr)
            continue
        out.write_text(text + "\n", encoding="utf-8")
        print(f"done  {out.relative_to(REPO_ROOT)}  ({len(text.split())} words)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
