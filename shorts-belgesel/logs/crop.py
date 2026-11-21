# crop the photo plates out of scanned book pages; a page may hold two plates stacked
import sys, os, numpy as np
from PIL import Image, ImageFilter
src, dst = sys.argv[1], sys.argv[2]
for f in sorted(os.listdir(src)):
    im = Image.open(os.path.join(src, f)).convert('L')
    a = np.asarray(im.filter(ImageFilter.BoxBlur(6)), dtype=np.float32)
    dark = a < 165
    rows = dark.mean(1) > 0.45; cols = dark.mean(0) > 0.30
    # contiguous runs of photo rows
    runs, start = [], None
    for i, v in enumerate(list(rows) + [False]):
        if v and start is None: start = i
        if not v and start is not None:
            if i - start > 250: runs.append((start, i))
            start = None
    for k, (r0, r1) in enumerate(runs):
        c = dark[r0:r1].mean(0) > 0.45
        idx = np.where(c)[0]
        if len(idx) < 250: continue
        box = (int(idx[0]) + 12, r0 + 12, int(idx[-1]) - 12, r1 - 12)
        name = f.split('-')[0] + (chr(97 + k) if len(runs) > 1 else '')
        im.crop(box).save(os.path.join(dst, name + '.jpg'), quality=93)
        print(name, box[2] - box[0], 'x', box[3] - box[1])
