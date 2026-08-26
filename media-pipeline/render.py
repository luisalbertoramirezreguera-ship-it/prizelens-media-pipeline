#!/usr/bin/env python3
from __future__ import annotations

import argparse
import subprocess
from pathlib import Path

import numpy as np
import soundfile as sf
from kokoro import KPipeline


def run(command: list[str]) -> None:
    subprocess.run(command, check=True)


def synthesize(text: str, output_wav: Path, voice: str, speed: float) -> None:
    pipeline = KPipeline(lang_code="a")
    chunks: list[np.ndarray] = []
    for _graphemes, _phonemes, audio in pipeline(text, voice=voice, speed=speed):
        chunks.append(np.asarray(audio, dtype=np.float32))
    if not chunks:
        raise RuntimeError("TTS produced no audio")
    sf.write(output_wav, np.concatenate(chunks), 24000, subtype="PCM_16")


def normalize_audio(source: Path, destination: Path) -> None:
    run(["ffmpeg", "-y", "-i", str(source), "-af", "loudnorm=I=-14:TP=-1.5:LRA=7", "-ar", "48000", "-ac", "2", str(destination)])


def render_video(image: Path, audio: Path, output: Path) -> None:
    run([
        "ffmpeg", "-y", "-loop", "1", "-framerate", "30", "-i", str(image), "-i", str(audio),
        "-vf", "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,format=yuv420p",
        "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-tune", "stillimage",
        "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", "-shortest", str(output)
    ])


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--image", required=True, type=Path)
    parser.add_argument("--text-file", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--voice", default="am_michael")
    parser.add_argument("--speed", type=float, default=1.05)
    args = parser.parse_args()

    text = args.text_file.read_text(encoding="utf-8").strip()
    if not text:
        raise ValueError("Transcript is empty")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    raw_wav = args.output.with_suffix(".raw.wav")
    normalized_wav = args.output.with_suffix(".wav")
    synthesize(text, raw_wav, args.voice, args.speed)
    normalize_audio(raw_wav, normalized_wav)
    render_video(args.image, normalized_wav, args.output)
    raw_wav.unlink(missing_ok=True)
    print(f"VIDEO={args.output}")
    print(f"AUDIO={normalized_wav}")


if __name__ == "__main__":
    main()
