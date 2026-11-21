# GTA-loading-screen style character scene (SD-Turbo text2img, CPU). usage: scene.py "<prompt>" <out_prefix> <seed1,seed2,...> [W H]
import sys, torch, time
from diffusers import AutoPipelineForText2Image
prompt, pre, seeds = sys.argv[1], sys.argv[2], [int(s) for s in sys.argv[3].split(',')]
w, h = (int(sys.argv[4]), int(sys.argv[5])) if len(sys.argv) > 5 else (512, 896)
torch.set_num_threads(4)
pipe = AutoPipelineForText2Image.from_pretrained('stabilityai/sd-turbo', variant='fp16', torch_dtype=torch.float32)
for s in seeds:
    t = time.time()
    im = pipe(prompt=prompt, num_inference_steps=4, guidance_scale=0.0, width=w, height=h, generator=torch.Generator().manual_seed(s)).images[0]
    im.save(f'{pre}_{s}.png'); print(s, round(time.time() - t, 1), flush=True)
