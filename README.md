# PrizeLens Media Pipeline

Zero-cost public rendering pipeline for PrizeLens educational social videos.

This repository contains no PrizeLens private source code, credentials, affiliate data, customer data, or production secrets.

Pipeline:

1. approved 9:16 slide + approved transcript;
2. local/open TTS generation;
3. loudness normalization;
4. FFmpeg 1080x1920 MP4 render;
5. GitHub Actions artifact containing MP4 + WAV;
6. artifact can be retrieved and passed to Metricool.

Routine renders use GitHub-hosted Actions on this public repository so they do not consume the private PrizeLens repository workflow minutes.
