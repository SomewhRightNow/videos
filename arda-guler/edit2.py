# Arda Güler free kick vs Belgium - pro vertical edit, real speed only (broadcaster logo kept visible)
import sys, os, subprocess, math
import numpy as np
sys.path.insert(0, '/home/user/Filmler/_engine')
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import engine as G
from engine import *
from PIL import Image, ImageDraw, ImageFilter, ImageChops

SRC = 'source.mp4'; SW, SH = 1128, 720
raw = subprocess.run(['ffmpeg', '-nostdin', '-loglevel', 'error', '-i', SRC, '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-r', '30', '-'], capture_output=True).stdout
FR = np.frombuffer(raw, np.uint8).reshape(-1, SH, SW, 3); NSRC = len(FR)
S0 = 1.0                      # source start
LIVE_END = 14.5               # output time where the live part ends
GOAL = 3.4 - S0               # output time of the goal
KICK = 1.7 - S0
FREEZE_SRC = 8.8
TOTAL_ = 19.5
RED = (227, 10, 23); BELY = (253, 218, 36); BELB = (20, 20, 20); BELR = (239, 51, 64)
CARD_W = 1040; CARD_H = int(SH * CARD_W / SW); CARD_Y = 1000 - CARD_H // 2

def rounded(im, r=26):
    m = Image.new('L', im.size, 0); ImageDraw.Draw(m).rounded_rectangle([0, 0, im.width - 1, im.height - 1], r, fill=255); im = im.convert('RGBA'); im.putalpha(m); return im

def flag_tr(w, h):
    f = Image.new('RGBA', (w, h), RED + (255,)); d = ImageDraw.Draw(f)
    cx, cy, r = w * 0.38, h / 2, h * 0.27
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=WHITE); r2 = r * 0.8; c2 = cx + r * 0.25
    d.ellipse([c2 - r2, cy - r2, c2 + r2, cy + r2], fill=RED + (255,))
    sx, sy, sr = w * 0.62, h / 2, h * 0.13
    pts = [(sx + sr * math.cos(math.radians(-90 + k * 36)) * (1 if k % 2 == 0 else 0.42), sy + sr * math.sin(math.radians(-90 + k * 36)) * (1 if k % 2 == 0 else 0.42)) for k in range(10)]
    d.polygon(pts, fill=WHITE); return rounded(f, 6)
def flag_be(w, h):
    f = Image.new('RGBA', (w, h)); d = ImageDraw.Draw(f)
    for k, col in enumerate([BELB, BELY, BELR]): d.rectangle([k * w / 3, 0, (k + 1) * w / 3, h], fill=col + (255,))
    return rounded(f, 6)
FTR, FBE = flag_tr(78, 52), flag_be(78, 52)

def bg_and_card(arr):
    im = Image.fromarray(arr)
    bg = im.resize((int(SW * 1920 / SH), 1920), Image.BILINEAR); bg = bg.crop(((bg.width - 1080) // 2, 0, (bg.width - 1080) // 2 + 1080, 1920)).filter(ImageFilter.GaussianBlur(30))
    bg = Image.eval(bg, lambda v: int(v * 0.32)).convert('RGBA')
    card = rounded(im.resize((CARD_W, CARD_H), Image.LANCZOS))
    sh = Image.new('RGBA', (CARD_W + 120, CARD_H + 120), (0, 0, 0, 0)); ImageDraw.Draw(sh).rounded_rectangle([60, 70, CARD_W + 60, CARD_H + 70], 26, fill=(0, 0, 0, 210))
    bg.alpha_composite(sh.filter(ImageFilter.GaussianBlur(26)), ((1080 - CARD_W) // 2 - 60, CARD_Y - 60))
    bg.alpha_composite(card, ((1080 - CARD_W) // 2, CARD_Y))
    d = ImageDraw.Draw(bg); d.rounded_rectangle([(1080 - CARD_W) // 2, CARD_Y, (1080 + CARD_W) // 2, CARD_Y + CARD_H], 26, outline=RED + (255,), width=5)
    return bg

def colour_pop(arr):
    a = arr.astype(np.float32); r, g, b = a[..., 0], a[..., 1], a[..., 2]
    redness = np.clip((r - np.maximum(g, b)) / 80.0, 0, 1)[..., None]
    grey = a.mean(2, keepdims=True) * 0.55
    return np.clip(grey * (1 - redness) + a * redness * 1.1, 0, 255).astype(np.uint8)

def scorebug(c, t):
    goal = t >= GOAL
    lay = Image.new('RGBA', (760, 96), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    d.rounded_rectangle([0, 0, 759, 95], 20, fill=(10, 12, 18, 235), outline=(255, 255, 255, 60), width=2)
    lay.alpha_composite(FTR, (22, 22)); lay.alpha_composite(FBE, (760 - 22 - 78, 22))
    f = font(F_BIG, 60)
    d.text((118, 14), 'TÜR', font=f, fill=WHITE + (255,)); d.text((760 - 118, 14), 'BEL', font=f, fill=WHITE + (255,), anchor='ra')
    pop = 1 + 0.35 * (1 - ease_out(prog(t, GOAL, GOAL + 0.35))) if goal else 1
    sc = text_img(f'{1 if goal else 0}  –  0', F_BIG, int(64 * pop), (GOAL_C if goal and t < GOAL + 2.5 else WHITE))
    lay.alpha_composite(sc, (380 - sc.width // 2, 48 - sc.height // 2))
    tag = text_img("20'", F_MONO, 26, (20, 20, 20), bar=BELY + (255,), pad=(10, 3));
    c.alpha_composite(lay, (160, CARD_Y - 140)); c.alpha_composite(tag, (160 + 760 - tag.width // 2 - 10, CARD_Y - 160))
GOAL_C = (120, 255, 140)

def lower_third(c, t, t_in, t_out, title, sub=None, col=RED):
    if t < t_in or t > t_out + 0.3: return
    p = ease_out(prog(t, t_in, t_in + 0.35)); a = 1 - clamp((t - t_out) / 0.3)
    lay = Image.new('RGBA', (1000, 190), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    w = int(980 * p); d.rectangle([0, 0, w, 110], fill=(10, 12, 18, 235)); d.rectangle([0, 0, 14, 110], fill=col + (255,))
    if p > 0.6: d.text((40, 14), title, font=font(F_BIG, 78), fill=WHITE + (255,))
    if sub and p > 0.8:
        d.rectangle([0, 110, min(w, 40 + int(font(F_MONO, 32).getlength(sub)) + 40), 165], fill=col + (255,))
        d.text((40, 118), sub, font=font(F_MONO, 32), fill=WHITE + (255,))
    c.alpha_composite(G._alpha(lay, a), (40, CARD_Y + CARD_H + 60))

def frame(t):
    if t < LIVE_END:
        k = min(NSRC - 1, int((S0 + t) * 30)); c = bg_and_card(FR[k])
    else:
        k = int(FREEZE_SRC * 30)
        c = bg_and_card(colour_pop(FR[k]))
    # shake + flash at goal
    dx = dy = 0
    for th, amp in [(KICK, 8), (GOAL, 24)]:
        if th <= t < th + 0.45: q = (t - th) / 0.45; dx += amp * (1 - q) ** 2 * math.sin(t * 90); dy += amp * (1 - q) ** 2 * math.cos(t * 77)
    if dx or dy: c = c.transform((W, H), Image.AFFINE, (1 / 1.03, 0, (W - W / 1.03) / 2 - dx, 0, 1 / 1.03, (H - H / 1.03) / 2 - dy), resample=Image.BILINEAR)
    a = np.asarray(c.convert('RGB')).astype(np.float32)
    fl = 0.5 * (1 - (t - GOAL) / 0.25) if GOAL <= t < GOAL + 0.25 else (0.6 * (1 - (t - LIVE_END) / 0.3) if LIVE_END <= t < LIVE_END + 0.3 else 0)
    if fl: a = a + (255 - a) * fl
    a = a * G.VIG[..., :]; g = G.GRAIN[int(t * 30) % 6]; a += np.repeat(np.repeat(g, 2, 0), 2, 1)[..., None] * 0.6
    c = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)).convert('RGBA')
    # overlays
    if t < LIVE_END:
        slam(c, t, -0.3, LIVE_END - 0.1, 'ARDA GÜLER', 250, 170, WHITE)
        label(c, t, 0.0, LIVE_END - 0.1, 'UEFA NATIONS LEAGUE · TONIGHT', W / 2, 375, 32, fill=GOLD)
        scorebug(c, t)
        slam(c, t, GOAL, GOAL + 1.6, 'GOAL!', CARD_Y + CARD_H // 2, 260, WHITE)
        lower_third(c, t, GOAL + 0.4, 7.4, 'TOP CORNER.', "20' · DIRECT FREE KICK · ~25 M")
        lower_third(c, t, 7.6, 10.9, 'TÜRKİYE 1–0 BELGIUM', 'ARDA GÜLER · TÜRKİYE', BELY)
        lower_third(c, t, 11.1, LIVE_END - 0.1, 'REVENGE ON?', 'OCTOBER · BELGIUM 3–0 TÜRKİYE', RED)
    else:
        slam(c, t, LIVE_END + 0.2, TOTAL_, 'BEST FREE KICK', 280, 140, WHITE)
        slam(c, t, LIVE_END + 0.5, TOTAL_, 'OF THE YEAR?', 420, 150, (255, 70, 70))
        label(c, t, LIVE_END + 0.9, TOTAL_, 'COMMENT BELOW', W / 2, 1660, 40)
        subscribe(c, t, LIVE_END + 1.2, y=1470)
        if t > LIVE_END + 1.2:
            im = text_img('@somewhrightnow', F_MONO, 34, CREAM); c.alpha_composite(G._alpha(im, clamp((t - LIVE_END - 1.2) / 0.4)), (int(W / 2 - im.width / 2), 1570))
    if t > TOTAL_ - 0.4: c = Image.blend(c, Image.new('RGBA', (W, H), (0, 0, 0, 255)), clamp((t - (TOTAL_ - 0.4)) / 0.4))
    return c.convert('RGB')

if __name__ == '__main__':
    if sys.argv[1] == 'probe':
        ts = [float(v) for v in sys.argv[2].split(',')]; ims = [frame(x).resize((270, 480)) for x in ts]
        s = Image.new('RGB', (270 * len(ims), 480)); [s.paste(im, (i * 270, 0)) for i, im in enumerate(ims)]; s.save('out/probe2.jpg')
    else:
        p = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', '1080x1920', '-r', '30', '-i', '-', '-c:v', 'libx264', '-preset', 'medium', '-crf', '18', '-pix_fmt', 'yuv420p', 'out/video2.mp4'], stdin=subprocess.PIPE)
        for f in range(int(TOTAL_ * 30)): p.stdin.write(frame(f / 30).tobytes())
        p.stdin.close(); p.wait()
        fc = (f"[0:a]aresample=48000,atrim={S0}:{S0 + TOTAL_},asetpts=PTS-STARTPTS,afade=t=out:st={LIVE_END + 1.5}:d=2.5[a1];"
              f"[1:a]aresample=48000,atrim=28:{28 + TOTAL_},asetpts=PTS-STARTPTS,volume='if(gte(t,{LIVE_END - 0.5}),0.35,0)':eval=frame,afade=t=out:st={TOTAL_ - 1.2}:d=1.2[a2];"
              "[a1][a2]amix=inputs=2:normalize=0,loudnorm=I=-14:TP=-1.2[aout]")
        subprocess.run(['ffmpeg', '-nostdin', '-y', '-loglevel', 'error', '-i', SRC, '-i', '/home/user/Filmler/football-war/audio/m_Volatile_Reaction.mp3', '-i', 'out/video2.mp4', '-filter_complex', fc, '-map', '2:v', '-map', '[aout]',
                        '-c:v', 'libx264', '-preset', 'slow', '-crf', '20', '-maxrate', '12M', '-bufsize', '24M', '-pix_fmt', 'yuv420p', '-movflags', '+faststart', '-c:a', 'aac', '-b:a', '192k', '-shortest', 'Arda Guler Free Kick vs Belgium (pro).mp4'])
        print('done')
