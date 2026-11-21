#!/bin/bash
# Optional AI tools (face swap, SD-Turbo, YOLO, SAM) + Claude skills. Run once in a fresh session: bash /home/user/Filmler/setup_ml.sh  (~3 GB)
set -e
# skills: cinematic-film (from this repo) + cinecode (GitHub)
mkdir -p ~/.claude/skills
cp -rn /home/user/Filmler/_skills/cinematic-film ~/.claude/skills/ 2>/dev/null || true
[ -d ~/.claude/skills/cinecode ] || git clone -q https://github.com/sarpstar/cinecode ~/.claude/skills/cinecode
# python env for image AI
V=/home/user/.sdvenv; [ -x $V/bin/python ] || python3 -m venv $V
$V/bin/pip install -q --index-url https://download.pytorch.org/whl/cpu torch torchvision
$V/bin/pip install -q diffusers transformers accelerate insightface onnxruntime opencv-python-headless ultralytics segment-anything pillow scipy
# models
export HF_HOME=/home/user/.hf; mkdir -p $HF_HOME /home/user/.yolo
$V/bin/python - <<'PY'
from huggingface_hub import hf_hub_download, snapshot_download
snapshot_download('stabilityai/sd-turbo', allow_patterns=['*.json','*fp16*','tokenizer/*','scheduler/*'])
hf_hub_download('ezioruan/inswapper_128.onnx', 'inswapper_128.onnx')
for f in ['gfpgan_1.4.onnx','real_esrgan_x2.onnx']: hf_hub_download('facefusion/models-3.0.0', f)
PY
cd /home/user/.yolo
for m in yolo11m-pose.pt yolo11m.pt; do [ -f $m ] || curl -sL -o $m https://github.com/ultralytics/assets/releases/download/v8.3.0/$m; done
[ -f sam_vit_b.pth ] || curl -sL -o sam_vit_b.pth https://dl.fbaipublicfiles.com/segment_anything/sam_vit_b_01ec64.pth
# insightface buffalo_l downloads itself on first use
echo "ml setup ok"
