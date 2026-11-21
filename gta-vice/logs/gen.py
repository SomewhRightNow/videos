# GTA-loading-screen style repaint of a real-photo composite (SD-Turbo img2img, CPU).
import sys, torch, time
from diffusers import AutoPipelineForImage2Image
from PIL import Image
init, out, prompt = sys.argv[1], sys.argv[2], sys.argv[3]
strength = float(sys.argv[4]) if len(sys.argv) > 4 else 0.5
seed = int(sys.argv[5]) if len(sys.argv) > 5 else 7
torch.set_num_threads(4)
pipe = AutoPipelineForImage2Image.from_pretrained('stabilityai/sd-turbo', variant='fp16', torch_dtype=torch.float32)
im = Image.open(init).convert('RGB').resize((576, 1024), Image.LANCZOS)
t = time.time()
r = pipe(prompt=prompt, image=im, num_inference_steps=4, strength=strength, guidance_scale=0.0, generator=torch.Generator().manual_seed(seed)).images[0]
r.save(out); print('done', round(time.time() - t, 1), 's')
