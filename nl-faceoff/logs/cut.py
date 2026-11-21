# BiRefNet background removal -> RGBA cutouts (assets/<key>_cut.png)
import sys
from rembg import remove, new_session
from PIL import Image
s = new_session('birefnet-general')
for k in sys.argv[1:]:
    im = Image.open(f'assets/{k}.jpg').convert('RGB')
    if max(im.size) > 1500: im.thumbnail((1500, 1500), Image.LANCZOS)
    out = remove(im, session=s, post_process_mask=True)
    bb = out.getbbox(); out = out.crop(bb); out.save(f'assets/{k}_cut.png'); print('cut', k, out.size, flush=True)
