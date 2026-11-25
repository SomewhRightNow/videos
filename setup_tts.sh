#!/usr/bin/env bash
# Chatterbox TTS (Resemble AI, MIT) kurulumu -> /home/user/.ttsvenv (bağımsız venv, ~1.5 GB) + modeller ~/.cache/huggingface (~6.3 GB).
# Idempotent: kuruluysa sadece kontrol eder. Kullanım: bash /home/user/Filmler/setup_tts.sh
set -e
V=/home/user/.ttsvenv
if [ -x $V/bin/python ] && $V/bin/python -c "import chatterbox.tts, chatterbox.mtl_tts, diffusers" 2>/dev/null; then
  echo "Chatterbox paketleri zaten kurulu."
else
  python3 -m venv $V
  P=$V/bin/pip
  $P install -q --upgrade pip
  $P install -q torch==2.11.0+cpu torchaudio==2.11.0+cpu torchvision==0.26.0+cpu --index-url https://download.pytorch.org/whl/cpu
  $P install -q "transformers==5.2.0" "tokenizers<0.23" "huggingface-hub<2" safetensors numpy scipy diffusers
  # chatterbox kendi pinlerini (torch 2.6) zorlamasın diye --no-deps; pip'in "incompatible" uyarıları beklenen durum.
  $P install -q chatterbox-tts==0.1.7 --no-deps
  $P install -q s3tokenizer resemble-perth conformer==0.3.2 omegaconf pyloudnorm librosa pykakasi einops soxr decorator joblib cloudpickle msgpack soundfile cffi
fi
# Modelleri indir (EN + TR multilingual) ve kısa test
cd "$(mktemp -d)"
$V/bin/python - <<'EOF'
import torch, soundfile as sf
torch.set_num_threads(4)
from chatterbox.tts import ChatterboxTTS
from chatterbox.mtl_tts import ChatterboxMultilingualTTS
m = ChatterboxTTS.from_pretrained(device='cpu'); w = m.generate("This is a short voice test.").squeeze(0).numpy(); print('EN ok', round(len(w)/m.sr, 2), 's'); del m
mm = ChatterboxMultilingualTTS.from_pretrained(device='cpu'); w = mm.generate("Bu kısa bir ses denemesi.", language_id='tr').squeeze(0).numpy(); print('TR ok', round(len(w)/mm.sr, 2), 's')
EOF
echo "Chatterbox hazır: $V/bin/python (örnek: fa1/logs/vo2.py, haaland/logs/tr_dub_cb.py)"
