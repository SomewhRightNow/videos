# face-aware crop of cutouts: head+shoulders, optional mirror so the player faces the centre. args: key:side (side L faces right, R faces left)
import sys, json, numpy as np
from PIL import Image
from insightface.app import FaceAnalysis
app = FaceAnalysis(name='buffalo_l', providers=['CPUExecutionProvider']); app.prepare(ctx_id=-1, det_size=(640, 640))
meta = {}
for spec in sys.argv[1:]:
    key, side = spec.split(':')
    c = Image.open(f'assets/{key}_cut.png').convert('RGBA')
    rgb = Image.new('RGB', c.size, (128, 128, 128)); rgb.paste(c, (0, 0), c)
    fs = app.get(np.asarray(rgb)[:, :, ::-1])
    if not fs: print('NO FACE', key); continue
    f = max(fs, key=lambda f: (f.bbox[2] - f.bbox[0]) * (f.bbox[3] - f.bbox[1]))
    x0, y0, x1, y1 = f.bbox; fw, fh = x1 - x0, y1 - y0; yaw = float(f.pose[1]) if f.pose is not None else 0.0
    nose = f.kps[2]; cx = (x0 + x1) / 2
    # insightface yaw: + = facing viewer's right, - = facing viewer's left; near-frontal faces are never mirrored (kit numbers)
    need = abs(yaw) > 12 and ((side == 'L' and yaw < 0) or (side == 'R' and yaw > 0))
    top = max(0, y0 - 0.75 * fh); bot = min(c.height, y1 + 2.6 * fh)
    l = max(0, cx - 1.9 * fw); r = min(c.width, cx + 1.9 * fw)
    cr = c.crop((int(l), int(top), int(r), int(bot)))
    fx = (cx - l) / cr.width; fy = ((y0 + y1) / 2 - top) / cr.height; fhr = fh / cr.height
    if need: cr = cr.transpose(Image.FLIP_LEFT_RIGHT); fx = 1 - fx
    cr.save(f'assets/{key}_prep.png')
    meta[key] = dict(side=side, flipped=bool(need), fx=float(fx), fy=float(fy), fh=float(fhr), w=cr.width, h=cr.height, yaw=float(yaw))
    print(key, side, 'flip' if need else 'keep', cr.size, f'yaw {yaw:.1f}', flush=True)
json.dump(meta, open('assets/prep.json', 'w'), indent=1)
