# AI subject cutout (rembg isnet) -> assets/cut/<key>.png at the size photo_img() will use
import sys, os
from rembg import remove, new_session
from PIL import Image
s = new_session('isnet-general-use')
for key in sys.argv[1:]:
    im = Image.open(f'assets/orig/{key}.jpg').convert('RGB')
    sc = max(1080 / im.width, 1920 / im.height) * 1.6
    if sc < 1: im = im.resize((int(im.width * sc), int(im.height * sc)), Image.LANCZOS)
    out = remove(im, session=s, alpha_matting=False)
    out.save(f'assets/cut/{key}.png'); print(key, out.size, out.getbbox(), flush=True)
