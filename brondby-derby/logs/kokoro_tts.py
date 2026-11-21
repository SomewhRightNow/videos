# Kokoro (Apache 2.0) narration, offline: python logs/kokoro_tts.py <voice> <speed> <out.wav> "<text>"
import sys, os, soundfile as sf
from kokoro_onnx import Kokoro
home = os.path.expanduser('~/.cinecode/kokoro')
k = Kokoro(os.path.join(home, 'kokoro-v1.0.onnx'), os.path.join(home, 'voices-v1.0.bin'))
voice, speed, out, text = sys.argv[1], float(sys.argv[2]), sys.argv[3], sys.argv[4]
lang = 'en-gb' if voice.startswith('b') else 'en-us'
samples, sr = k.create(text, voice=voice, speed=speed, lang=lang)
sf.write(out, samples, sr)
print(out, round(len(samples) / sr, 2), 's')
