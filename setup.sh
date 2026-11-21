#!/bin/bash
# Somewhere Right Now workspace setup for a fresh Claude Code cloud session. Run from the workspace checkout: bash setup.sh
set -e; HERE="$(cd "$(dirname "$0")" && pwd)"
# workspace is cloned directly into /home/user/Filmler; nothing to copy
FD=/mnt/skills/examples/canvas-design/canvas-fonts; mkdir -p "$FD" 2>/dev/null && cp -n /home/user/Filmler/fonts/* "$FD"/ 2>/dev/null || echo "font dir not writable: edit FD paths"
pip install -q numpy scipy pillow yt-dlp
K=~/.cinecode/kokoro; mkdir -p $K
[ -x $K/venv/bin/python ] || python3 -m venv $K/venv
$K/venv/bin/pip install -q kokoro-onnx soundfile
R=https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0
[ -f $K/kokoro-v1.0.onnx ] || curl -sL -o $K/kokoro-v1.0.onnx $R/kokoro-v1.0.onnx
[ -f $K/voices-v1.0.bin ] || curl -sL -o $K/voices-v1.0.bin $R/voices-v1.0.bin
which ffmpeg >/dev/null || (apt-get update -qq && apt-get install -y -qq ffmpeg)
echo "setup ok"
bash /home/user/Filmler/_sync/srn_sync.sh pull
