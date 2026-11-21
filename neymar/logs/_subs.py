# ---------------------------------------------------------------- bilingual subtitles
def _sent(s): return [p for p in re.split(r'(?<=[.?!])\s+', s.strip()) if p]
SUBS = []
for i, (en, tr) in enumerate(ROWS, 1):
    if i in CH: continue
    for k, v in DISPLAY.items(): en = en.replace(k, v)
    es, ts = _sent(en), _sent(tr)
    words = G.WORDS[i]
    if len(es) == len(ts) and len(es) > 1:
        idx = 0; starts = []
        for s_ in es: starts.append(words[min(idx, len(words) - 1)][1]); idx += len(s_.split())
        for j, (e_, t_) in enumerate(zip(es, ts)):
            a = starts[j] - 0.05; b = starts[j + 1] - 0.05 if j + 1 < len(es) else E(i) + 0.35
            SUBS.append((a, b, e_, t_))
    else: SUBS.append((L(i) - 0.05, E(i) + 0.35, en, tr))
def wrap(s, f, maxw):
    out, cur = [], ''
    for w_ in s.split():
        if f.getlength((cur + ' ' + w_).strip()) <= maxw: cur = (cur + ' ' + w_).strip()
        else: out.append(cur); cur = w_
    return out + [cur]
def subtitles(c, t):
    for a, b, en, tr in SUBS:
        if a <= t < b:
            fe, ft = font(F_T, 42), font(F_TI, 34)
            le, lt = wrap(en, fe, 1500), []; y = H - 70 - 54 * len(le)
            y0 = int(y) - 10; lay = Image.new('RGBA', (W, H - y0), (0, 0, 0, 0)); d = ImageDraw.Draw(lay); y -= y0
            for ln in le: d.text((W / 2, y), ln, font=fe, fill=WH + (255,), anchor='mt', stroke_width=4, stroke_fill=(0, 0, 0, 255)); y += 52
            y += 4
            for ln in lt: d.text((W / 2, y), ln, font=ft, fill=GOLD2 + (255,), anchor='mt', stroke_width=4, stroke_fill=(0, 0, 0, 255)); y += 44
            c.alpha_composite(lay, (0, y0)); return
