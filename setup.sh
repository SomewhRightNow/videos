#!/bin/bash
# Somewhere Right Now workspace setup for a fresh Claude Code cloud session. Run from the workspace checkout: bash setup.sh
set -e; HERE="$(cd "$(dirname "$0")" && pwd)"
mkdir -p /home/user/Filmler/_engine/tools /home/user/Filmler/_live
cp "$HERE"/engine/engine.py /home/user/Filmler/_engine/; cp "$HERE"/engine/tools/*.py /home/user/Filmler/_engine/tools/
cp "$HERE"/live/watch.py /home/user/Filmler/_live/; cp -n "$HERE"/OPERASYON.md /home/user/Filmler/ 2>/dev/null || true
cp -rn "$HERE"/projects/* /home/user/Filmler/ 2>/dev/null || true
FD=/mnt/skills/examples/canvas-design/canvas-fonts; mkdir -p "$FD" 2>/dev/null && cp -n "$HERE"/fonts/* "$FD"/ 2>/dev/null || echo "font dir not writable: edit FD paths"
pip install -q numpy scipy pillow yt-dlp
K=~/.cinecode/kokoro; mkdir -p $K
[ -x $K/venv/bin/python ] || python3 -m venv $K/venv
$K/venv/bin/pip install -q kokoro-onnx soundfile
R=https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0
[ -f $K/kokoro-v1.0.onnx ] || curl -sL -o $K/kokoro-v1.0.onnx $R/kokoro-v1.0.onnx
[ -f $K/voices-v1.0.bin ] || curl -sL -o $K/voices-v1.0.bin $R/voices-v1.0.bin
which ffmpeg >/dev/null || (apt-get update -qq && apt-get install -y -qq ffmpeg)
echo "setup ok"
