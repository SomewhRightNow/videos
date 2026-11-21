# ---------------------------------------------------------------- graphic helpers
def fade_in(t, a, d=0.25): return ease_out(prog(t, a, a + d))
def txt(c, s, path, size, fill, x, y, anchor='mm', alpha=1.0, stroke=0, sfill=(0, 0, 0)):
    if alpha <= 0: return
    f = font(path, size); l, tp, r, b = ImageDraw.Draw(c).textbbox((x, y), s, font=f, anchor=anchor, stroke_width=stroke)
    l, tp = int(l) - 4, int(tp) - 4; lay = Image.new('RGBA', (int(r) - l + 8, int(b) - tp + 8), (0, 0, 0, 0))
    ImageDraw.Draw(lay).text((x - l, y - tp), s, font=f, fill=fill + (int(255 * alpha),), anchor=anchor, stroke_width=stroke, stroke_fill=sfill + (int(255 * alpha),))
    c.alpha_composite(lay, (max(0, l), max(0, tp)), (max(0, -l), max(0, -tp)))
def wipe(c, t, t_in, s, x, y, size, fill=WH, path=F_H, bar=None, anchor='c', t_out=1e9):
    if not (t_in <= t < t_out): return
    p = ease_out(prog(t, t_in, t_in + 0.3)); im = text_img(s, path, size, fill, bar=bar, pad=(24, 6))
    v = Image.new('RGBA', im.size, (0, 0, 0, 0)); v.alpha_composite(im, (0, int((1 - p) * im.height)))
    if t_out < 1e8: v = G._alpha(v, 1 - prog(t, t_out - 0.25, t_out))
    v = shadowed(v, 12, 0.6); ox = {'c': v.width / 2, 'l': 14, 'r': v.width - 14}[anchor]
    c.alpha_composite(v, (int(x - ox), int(y - v.height / 2)))
def lower_third(c, t, t_in, t_out, title, sub, col=GOLD2):
    if not (t_in <= t < t_out): return
    p = ease_out(prog(t, t_in, t_in + 0.4)); a = 1 - prog(t, t_out - 0.3, t_out)
    lay = Image.new('RGBA', (W, 260), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    f1 = font(F_H, 44); f2 = font(F_MONO, 22); w = max(f1.getlength(title), f2.getlength(sub)) + 70
    x0 = 90; y0 = 120; d.rectangle([x0, y0, x0 + 8, y0 + 96], fill=col + (int(255 * a),))
    d.rectangle([x0 + 8, y0, x0 + 8 + w * p, y0 + 96], fill=(0, 0, 0, int(170 * a)))
    if p > 0.5:
        d.text((x0 + 34, y0 + 32), title, font=f1, fill=WH + (int(255 * a * prog(p, 0.5, 1)),), anchor='lm')
        d.text((x0 + 34, y0 + 74), sub, font=f2, fill=col + (int(255 * a * prog(p, 0.5, 1)),), anchor='lm')
    c.alpha_composite(lay)
def flag(code, w, h):
    f = Image.new('RGBA', (w, h), (255, 255, 255, 255)); d = ImageDraw.Draw(f)
    if code == 'ARG':
        d.rectangle([0, 0, w, h / 3], fill=SKY); d.rectangle([0, 2 * h / 3, w, h], fill=SKY); r = h * 0.12; d.ellipse([w / 2 - r, h / 2 - r, w / 2 + r, h / 2 + r], fill=(246, 180, 14))
    elif code == 'URU':
        for k in range(9): d.rectangle([0, k * h / 9, w, (k + 1) * h / 9], fill=WH if k % 2 == 0 else (0, 56, 168))
        d.rectangle([0, 0, w * 0.4, h * 5 / 9], fill=WH); r = h * 0.17; d.ellipse([w * 0.2 - r, h * 5 / 18 - r, w * 0.2 + r, h * 5 / 18 + r], fill=(252, 209, 22))
    elif code == 'POR':
        d.rectangle([0, 0, w * 0.4, h], fill=(0, 102, 0)); d.rectangle([w * 0.4, 0, w, h], fill=(218, 41, 28)); r = h * 0.26
        d.ellipse([w * 0.4 - r, h / 2 - r, w * 0.4 + r, h / 2 + r], fill=(255, 210, 0)); r2 = r * 0.6; d.ellipse([w * 0.4 - r2, h / 2 - r2, w * 0.4 + r2, h / 2 + r2], fill=(218, 41, 28))
    elif code == 'DEN':
        d.rectangle([0, 0, w, h], fill=(198, 12, 48)); d.rectangle([w * 0.3, 0, w * 0.3 + h * 0.18, h], fill=WH); d.rectangle([0, h * 0.41, w, h * 0.59], fill=WH)
    elif code == 'ESP':
        d.rectangle([0, 0, w, h], fill=(170, 21, 27)); d.rectangle([0, h / 4, w, 3 * h / 4], fill=(241, 191, 0))
    elif code == 'FRA':
        d.rectangle([0, 0, w / 3, h], fill=(0, 85, 164)); d.rectangle([2 * w / 3, 0, w, h], fill=(239, 65, 53))
    m = Image.new('L', (w, h), 0); ImageDraw.Draw(m).rounded_rectangle([0, 0, w - 1, h - 1], 8, fill=255); f.putalpha(m); return f
def scorebox(c, t, t_in, a, b, sa, sb, x, y, foot='', scale=1.0, t_out=1e9, win_b=True):
    if not (t_in <= t < t_out): return
    p = ease_out(prog(t, t_in, t_in + 0.35)); w, h = 760, 170
    lay = Image.new('RGBA', (w, h + 44), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    d.rounded_rectangle([0, 0, w - 1, h - 1], 22, fill=(8, 10, 16, 235), outline=(255, 255, 255, 70), width=2)
    lay.alpha_composite(flag(a, 90, 60), (28, 55)); lay.alpha_composite(flag(b, 90, 60), (w - 118, 55))
    d.text((134, h / 2), a, font=font(F_H, 60), fill=WH + (255,), anchor='lm'); d.text((w - 134, h / 2), b, font=font(F_H, 60), fill=WH + (255,), anchor='rm')
    d.text((w / 2 - 62, h / 2 + 4), str(sa), font=font(F_MEGA, 76), fill=(WH if win_b else GOLD2) + (255,), anchor='mm')
    d.text((w / 2, h / 2), '–', font=font(F_H, 60), fill=GRY + (255,), anchor='mm')
    d.text((w / 2 + 62, h / 2 + 4), str(sb), font=font(F_MEGA, 76), fill=((255, 90, 100) if win_b else WH) + (255,), anchor='mm')
    if foot: d.text((w / 2, h + 24), foot, font=font(F_MONO, 22), fill=WH + (255,), anchor='mm')
    if t_out < 1e8: lay = G._alpha(lay, 1 - prog(t, t_out - 0.25, t_out))
    place(c, shadowed(lay, 16), x, y + (1 - p) * 40, scale * (1.06 - 0.06 * p), p)
def counter_txt(c, t, t_in, v, x, y, size, fill, dur=1.2, fmt='{:d}', path=F_MEGA, t_out=1e9):
    if not (t_in <= t < t_out): return
    p = ease_out(prog(t, t_in, t_in + dur)); a = fade_in(t, t_in, 0.2) * (1 - prog(t, t_out - 0.25, t_out))
    txt(c, fmt.format(int(round(v * p))), path, size, fill, x, y, alpha=a)
def stamp(c, t, t_in, s, x, y, size=110, col=RED2, rot=-8, t_out=1e9):
    if not (t_in <= t < t_out): return
    p = ease_out(prog(t, t_in, t_in + 0.18)); im = text_img(s, F_H, size, WH, bar=col + (235,), pad=(30, 10))
    if t_out < 1e8: im = G._alpha(im, 1 - prog(t, t_out - 0.25, t_out))
    place(c, shadowed(im, 14), x, y, 1.8 - 0.8 * p, clamp((t - t_in) / 0.06), rot)
def quote(c, t, t_in, line1, line2, who, x=W * 0.30, t_out=1e9):
    if not (t_in <= t < t_out): return
    a = fade_in(t, t_in, 0.5) * (1 - prog(t, t_out - 0.3, t_out))
    shade(c, 'left' if x < W / 2 else 'right', 0.85 * a)
    txt(c, '“', F_H, 200, GOLD2, x - 380, 330, alpha=a)
    txt(c, line1, F_TI, 52, WH, x, 420, alpha=a); txt(c, line2, F_TI, 52, WH, x, 492, alpha=a)
    txt(c, who, F_MONO, 26, GOLD2, x, 590, alpha=a)
_SH = {}
def shade(c, where, a=0.8):
    if where not in _SH:
        g = np.zeros((H, W, 4), np.uint8); xx = np.linspace(0, 1, W)
        k = np.clip(1 - xx / 0.62, 0, 1) if where == 'left' else np.clip((xx - 0.38) / 0.62, 0, 1) if where == 'right' else None
        if where == 'bottom':
            yy = np.linspace(0, 1, H); g[..., 3] = (np.clip((yy - 0.72) / 0.28, 0, 1) ** 1.3 * 200)[:, None].astype(np.uint8)
        else: g[..., 3] = (k ** 1.2 * 230)[None, :].astype(np.uint8)
        _SH[where] = Image.fromarray(g, 'RGBA')
    c.alpha_composite(G._alpha(_SH[where], a) if a < 0.999 else _SH[where])
def polaroid(c, t, t_in, t_out, key, cap, x, y, rot, f=(0.5, 0.4)):
    if not (t_in <= t < t_out): return
    p = ease_out(prog(t, t_in, t_in + 0.45)); a = 1 - prog(t, t_out - 0.3, t_out)
    ph = cover(key, 0, 0, 1, 1.0, 1.0, *f, size=(420, 420))
    fr = Image.new('RGBA', (450, 520), (246, 242, 232, 255)); fr.paste(ph, (15, 15))
    ImageDraw.Draw(fr).text((225, 478), cap, font=font(F_MONO, 22), fill=(40, 40, 40, 255), anchor='mm')
    place(c, shadowed(G._alpha(fr, a), 18), x - (1 - p) * 80, y, 1.0, p, rot)
def chapter(c, t):
    for i, (n, en, tr) in CH.items():
        a0, a1 = S[i] - 0.3, S[i + 1] - 0.3
        if a0 <= t < a1:
            a = fade_in(t, a0, 0.4) * (1 - prog(t, a1 - 0.35, a1))
            p = ease_out(prog(t, a0, a0 + 0.8))
            im = text_img(n, F_MEGA, 300, (255, 255, 255, 0), stroke=4, stroke_fill=GOLD2)
            place(c, G._alpha(im, a * 0.9), W / 2, 380, 1.15 - 0.15 * p, 1.0)
            txt(c, en, F_H, 104, WH, W / 2, 620, alpha=a)
            ImageDraw.Draw(c).rectangle([W / 2 - 300 * p, 760, W / 2 + 300 * p, 763], fill=GOLD2 + (int(200 * a),))
def badge(c, t):
    if S[26] <= t < S[32] - 0.4:
        lay = text_img('●  FILMED BY US · ESTÁDIO MUNICIPAL DE BRAGA · 14.11.2026', F_MONO, 22, WH, bar=(0, 0, 0, 170), pad=(16, 8))
        if int(t * 2) % 2 == 0: ImageDraw.Draw(lay).ellipse([14, lay.height / 2 - 8, 30, lay.height / 2 + 8], fill=RED2 + (255,))
        c.alpha_composite(lay, (W - lay.width - 60, 60))
def gev_credit(c, t):
    if t < S[4] or S[6] <= t < S[8]:
        txt(c, 'GLOBE: GOD\'S EYE VIEW · IMAGERY © ESRI, MAXAR, EARTHSTAR GEOGRAPHICS', F_MONO, 16, GRY, W - 40, H - 22, anchor='rm', alpha=0.9)
