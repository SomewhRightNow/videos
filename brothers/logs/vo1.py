import os, sys, soundfile as sf
from kokoro_onnx import Kokoro
home = os.path.expanduser('~/.cinecode/kokoro')
k = Kokoro(os.path.join(home, 'kokoro-v1.0.onnx'), os.path.join(home, 'voices-v1.0.bin'))
a, sr = k.create(sys.argv[2], voice='bm_lewis', speed=0.98, lang='en-gb'); sf.write(sys.argv[1], a, sr); print(round(len(a)/sr,2))
