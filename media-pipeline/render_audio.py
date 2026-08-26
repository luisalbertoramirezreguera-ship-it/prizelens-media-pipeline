#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

from render import synthesize, normalize_audio


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--text-file", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--voice", default="am_michael")
    parser.add_argument("--speed", type=float, default=1.05)
    args = parser.parse_args()

    text = args.text_file.read_text(encoding="utf-8").strip()
    if not text:
        raise ValueError("Transcript is empty")

    args.output.parent.mkdir(parents=True, exist_ok=True)
    raw = args.output.with_suffix(".raw.wav")
    synthesize(text, raw, args.voice, args.speed)
    normalize_audio(raw, args.output)
    raw.unlink(missing_ok=True)
    print(f"AUDIO={args.output}")


if __name__ == "__main__":
    main()
