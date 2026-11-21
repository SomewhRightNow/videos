# rembg cutouts -> assets/cut/<key>.png (cropped to the subject)
import sys, glob, os
from rembg import new_session, remove
from PIL import Image
s = new_session('isnet-general-use')
for f in sorted(glob.glob('assets/orig/p_*.jpg')):
    k = os.path.basename(f)[:-4]; out = f'assets/cut/{k}.png'
    if os.path.exists(out) or open(f,'rb').read(2)!=b'\xff\xd8': continue
    im = Image.open(f).convert('RGB')
    r = remove(im, session=s, post_process_mask=True)
    a = r.split()[3].point(lambda v: 255 if v > 140 else (0 if v < 30 else v))
    import numpy as np
    from scipy.ndimage import label
    m = np.asarray(a) > 60; lab, n = label(m)
    if n > 1:
        sizes = [(lab == i).sum() for i in range(1, n + 1)]; keep = 1 + int(np.argmax(sizes))
        arr = np.asarray(a).copy(); arr[(lab != keep) & (lab > 0)] = 0; a = Image.fromarray(arr)
    r.putalpha(a); bb = a.getbbox(); r = r.crop(bb); r.save(out); print(k, r.size, flush=True)
