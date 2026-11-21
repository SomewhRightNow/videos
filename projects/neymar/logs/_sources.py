# ---------------------------------------------------------------- sources
_IM = {}
def photo(key):
    if key not in _IM: _IM[key] = Image.open(f'assets/orig/{key}.jpg').convert('RGB')
    return _IM[key]
def cover(key, t, a, b, z0=1.0, z1=1.12, fx=0.5, fy=0.4, size=(W, H), bw=False, dx=0.0):
    im = photo(key); bw_, bh = size
    s = max(bw_ / im.width, bh / im.height) * lerp(z0, z1, ease_io(prog(t, a, b)))
    vw, vh = bw_ / s, bh / s; cx = clamp(im.width * (fx + dx * prog(t, a, b)), vw / 2, im.width - vw / 2); cy = clamp(im.height * fy, vh / 2, im.height - vh / 2)
    out = im.crop((int(cx - vw / 2), int(cy - vh / 2), int(cx + vw / 2), int(cy + vh / 2))).resize(size, Image.LANCZOS)
    return out.convert('L').convert('RGB') if bw else out
_BLUR = {}
def blurred(key, k=0.35):
    if key not in _BLUR:
        im = cover(key, 0, 0, 1, 1.0, 1.0, size=(W // 4, H // 4)).filter(ImageFilter.GaussianBlur(10)).resize((W, H), Image.BILINEAR)
        _BLUR[key] = Image.eval(im, lambda v: int(v * k))
    return _BLUR[key].copy()
def side(key, t, a, b, where='right', fx=0.5, fy=0.3, z0=1.0, z1=1.1, frac=0.5, bw=False, k=0.35):
    """portrait photo filling one side, blurred copy behind, soft seam"""
    bg = blurred(key, k); pw = int(W * frac)
    ph = cover(key, t, a, b, z0, z1, fx, fy, size=(pw, H), bw=bw)
    m = Image.new('L', (pw, H), 255); md = ImageDraw.Draw(m)
    for i in range(160):
        x = i if where == 'right' else pw - 1 - i; md.line([(x, 0), (x, H)], fill=int(255 * i / 160))
    bg.paste(ph, (W - pw, 0) if where == 'right' else (0, 0), m)
    return bg.convert('L').convert('RGB') if bw else bg
def split2(k1, k2, t, a, b, f1=(0.5, 0.3), f2=(0.5, 0.3), bw=False):
    l = cover(k1, t, a, b, 1.0, 1.08, *f1, size=(W // 2, H), bw=bw); r = cover(k2, t, a, b, 1.0, 1.08, *f2, size=(W // 2, H), bw=bw)
    im = Image.new('RGB', (W, H)); im.paste(l, (0, 0)); im.paste(r, (W // 2, 0)); ImageDraw.Draw(im).rectangle([W // 2 - 3, 0, W // 2 + 3, H], fill=(0, 0, 0))
    return im
_FR = {}
def gev(seq, t, t0):
    d = f'src/gev/{seq}_30'; n = len(os.listdir(d)) if os.path.isdir(d) else 0
    if n == 0: return Image.new('RGB', (W, H), (8, 10, 14))
    k = min(n, max(1, int((t - t0) * 30) + 1)); key = (seq, k)
    if key not in _FR:
        if len(_FR) > 60: _FR.clear()
        _FR[key] = Image.open(f'{d}/f_{k:04d}.jpg').convert('RGB').resize((W, H))
    return _FR[key]
FOOT = {'fa': ('/home/user/Filmler/obrigado-capitao/src/fa', 150), 'fb': ('/home/user/Filmler/obrigado-capitao/src/fb', 105),
        'lu': ('/home/user/Filmler/portugal-1-4/src2/lu', 210), 'wk': ('/home/user/Filmler/portugal-1-4/src2/wk', 120)}
def footage(folder, t, t0, speed=1.0, start=1, dim=1.0):
    """user's vertical stadium footage inside a 16:9 frame: blurred fill + sharp centre panel"""
    path, n = FOOT[folder]; k = min(n, max(1, int((t - t0) * 30 * speed) + start))
    key = ('ft', folder, k)
    if key not in _FR:
        if len(_FR) > 60: _FR.clear()
        _FR[key] = Image.open(f'{path}/f_{k:04d}.jpg').convert('RGB')
    fr = _FR[key]
    q = fr.resize((W // 4, int(W // 4 * fr.height / fr.width)), Image.BILINEAR); oy = (q.height - H // 4) // 2
    bg = Image.eval(q.crop((0, oy, W // 4, oy + H // 4)).filter(ImageFilter.GaussianBlur(7)), lambda v: int(v * 0.4)).resize((W, H), Image.BILINEAR)
    ph = int(H * 0.96); pw = int(ph * fr.width / fr.height); pan = fr.resize((pw, ph), Image.LANCZOS)
    if dim != 1.0: pan = Image.eval(pan, lambda v: int(v * dim))
    bg.paste(pan, ((W - pw) // 2, (H - ph) // 2)); ImageDraw.Draw(bg).rectangle([(W - pw) // 2 - 3, (H - ph) // 2 - 3, (W + pw) // 2 + 2, (H + ph) // 2 + 2], outline=(255, 255, 255))
    return bg
def dark(t, col=(14, 14, 22)):
    if 'dark' not in _BLUR:
        yy, xx = np.mgrid[0:H, 0:W].astype(np.float32); r = np.sqrt(((xx - W / 2) / W) ** 2 + ((yy - H / 2) / H) ** 2)
        k = np.clip(1 - r * 1.3, 0, 1)[..., None]; _BLUR['dark'] = Image.fromarray((np.array((4, 4, 8), np.float32) * (1 - k) + np.array(col, np.float32) * k).astype(np.uint8))
    return _BLUR['dark']
