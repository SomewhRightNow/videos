# Builds <film>/film.html from strange-laws' film.html with a new FILM section. python3 build.py <film-dir>
# spec: <film-dir>/logs/spec.py defines TITLE, LINES, GAPS(optional), SHOTS(list of [key, to, z0,z1,fx0,fx1,fy0,fy1]), TITLES, SFX_EXTRA, BLOOP
import sys, os, json, subprocess, importlib.util
film = os.path.abspath(sys.argv[1]); tpl = open('/home/user/Filmler/strange-laws/film.html').read()
spec = importlib.util.spec_from_file_location('spec', os.path.join(film, 'logs/spec.py')); S = importlib.util.module_from_spec(spec); spec.loader.exec_module(S)
dur = lambda f: float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',f]).decode())
VD = [round(dur(os.path.join(film, f'audio/vo-t/VO{i+1}.wav')), 2) for i in range(len(S.LINES))]
VT = []; t = 0.15
for i, d in enumerate(VD):
    t += S.PAUSE.get(i, 0) if hasattr(S, 'PAUSE') else 0
    VT.append(round(t, 2)); t = t + d + 0.35
DURATION = round(VT[-1] + VD[-1] + S.TAIL, 2)
# shots: times given as VO anchors 'v3' (= start of VO3) or numbers; last shot runs to the end
def at(x):
    if isinstance(x, str) and x.startswith('v'):
        n, _, off = x[1:].partition('+'); return round(VT[int(n)-1] - 0.05 + (float(off) if off else 0), 2)
    return x
shots = []; prev = 0.0
for k, (key, to, *mv) in enumerate(S.SHOTS):
    end = DURATION if to == 'end' else at(to); shots.append([key, round(prev,2), end, *mv]); prev = end
titles = [[s, at(a), (DURATION if b == 'end' else at(b)), y, size, col, kind] for s, a, b, y, size, col, kind in S.TITLES]
keys = sorted({s[0] for s in shots})
chap = [{'chapter': f'S{i+1}', 'from': VT[i] if i else 0, 'to': (VT[i+1] if i+1 < len(VT) else DURATION)} for i in range(len(VT))]
J = lambda o: json.dumps(o, ensure_ascii=False)
film_src = f"""// ============================== FILM ==============================
const TITLE = {J(S.TITLE)};
const PURPOSE = 'cinematic';
// Real photographs only (open licences / public domain archives), graded, type over picture.
const LOOKS = {{
  'abyss': {{ grade: {J(getattr(S, 'GRADE', 'saturate(1.05) contrast(1.1) brightness(0.92)'))}, bloom: 0.1, texture: null, vignette: 0.62, grain: 0.07, grainHold: 1, hold: 24, line: 0, steps: 0,
    palette: {{ bg: '#020a12', ink: '#ffffff', accent: '#7fe3ff', dim: '#ff4d4d' }} }},
}};
const LOOK_ID = 'abyss';
const LOOK = LOOKS[LOOK_ID];
const FINISH = {{ shutter: null, weave: 0.5, tone: null }};
const FPS = 24;
const DURATION = {DURATION};
const BPM = 80;                              // "Music For Unknown Documentary Films" (Ambient Samurai); the cuts follow the narration
const BEAT0 = 0;
const beat = (n) => BEAT0 + n * 60 / BPM, bar = (n) => beat(4 * n);
const OWN_MUSIC = {{ file: 'audio/music.wav', gain: 0.55 }};
const INSTRUMENTS = [];
const CAST = {{}};
const FORMULAS = {{}};
const PALETTE = {{ ...LOOK.palette, ice: {J(getattr(S, 'ACCENT', '#7fe3ff'))}, red: '#ff4d4d' }};
const CLOCKS = {J([[at(a), (DURATION if b=='end' else at(b)), s0, r, y, sz, c] for a, b, s0, r, y, sz, c in getattr(S, 'CLOCKS', [])])};
const BELLS = {J([at(x) for x in getattr(S, 'BELLS', [])])};
const FLASHES = {J([[at(a), d] for a, d in getattr(S, 'FLASHES', [])])};
const TYPE = {{
  lang: 'en',
  roles: {{
    display: {{ family: 'Big Shoulders Display', pkg: 'big-shoulders-display', version: '5.3.0', weights: [700, 900] }},
    text: {{ family: 'Familjen Grotesk', pkg: 'familjen-grotesk', version: '5.3.0', weights: [500, 600, 700] }},
    mono: null,
  }},
  check: {{ strings: {{ display: {J([t[0] for t in titles][:8])} }}, sizes: {{ text: 0.04 }} }},
}};
const KEYS = {J(keys)};
const PHOTO_FILES = Object.fromEntries(KEYS.map((k) => [k, 'assets/img/' + k + '.jpg']));
const PH = {{}}, MAP = {{}};
function loadPhotos() {{
  return Promise.all(Object.entries(PHOTO_FILES).map(([k, src]) => new Promise((ok, fail) => {{
    const i = new Image();
    i.onload = () => {{
      const s = Math.min(1, 2200 / Math.max(i.width, i.height)), c = Object.assign(document.createElement('canvas'), {{ width: Math.round(i.width * s), height: Math.round(i.height * s) }});
      const x = c.getContext('2d'); x.imageSmoothingQuality = 'high'; x.drawImage(i, 0, 0, c.width, c.height); PH[k] = c; ok();
    }};
    i.onerror = () => fail(new Error('photo: ' + src)); i.src = src;
  }})));
}}
function loadMap() {{ return Promise.resolve(); }}
const VT = {J(VT)};
const VD = {J(VD)};
const VO = VT.map((at, i) => ({{ id: 'VO' + (i + 1), at, dur: VD[i] }}));
const LINES = {J(S.LINES)};
const SUBS = LINES.map((text, i) => ({{ at: VT[i], to: VT[i] + VD[i] + 0.3, text }}));
const CAPTIONS = null;
const CAPTION_STYLE = {{ role: 'text', accentRole: 'text', size: 0.05, caps: false, ink: PALETTE.ink, hi: PALETTE.ink, accent: PALETTE.accent, punch: 0 }};
// [key, from, to, zoom from, zoom to, focus x from, to, focus y from, to]
const SHOTS = {J(shots)};
const XF = 0.25;
const END_AT = {at(S.END_AT)};
const SCENES = {J(chap)}.map((s) => ({{ ...s, draw: reel, action: 'photo with a slow camera move and a type slam' }}));
const SFX = [
  ...{J([at(x) for x in getattr(S, 'HITS', [])])}.map((at) => ({{ at, voice: 'hit', gain: 0.32, wet: 0.35 }})),
  ...{J([at(x) for x in getattr(S, 'TICKS', [])])}.map((at) => ({{ at, voice: 'tick', gain: 0.25, wet: 0.25 }})),
  ...{J([at(x) for x in getattr(S, 'WHOOSH', [])])}.map((at) => ({{ at: at - 0.25, voice: 'whoosh', dur: 0.5, gain: 0.14, wet: 0.3 }})),
  ...{J([dict(e, at=at(e['at'])) for e in S.SFX_EXTRA])},
];
const CLOCK_TICKS = CLOCKS.flatMap(([a, b, s0, r]) => r > 0 && r <= 2 ? Array.from({{ length: Math.floor((b - a) * r) }}, (_, i) => a + (i + 1 - (s0 % 1)) / r).filter((x) => x < b) : []);
SFX.push(...CLOCK_TICKS.map((at) => ({{ at, voice: 'tick', gain: 0.22, wet: 0.15 }})));
const ROOM = {{ secs: 3.0, decay: 3.5, tone: 2600 }};
const ARRANGEMENT = [{{ section: 'whole', from: 0, to: DURATION, parts: [] }}];

// ---------- the film's own drawing ----------
const CXc = 0.46;
const popIn = (t, at, d = 0.3) => {{ const k = MOTION.at(t, at, d); return k <= 0 ? 0 : MOTION.back(k, 1.6); }};
const slam = (t, at) => {{ const s = MOTION.at(t, at, 0.16); return s <= 0 ? 0 : lerp(1.6, 1, EASE.out(s)); }};
function photo(g, img, z, fx = 0.5, fy = 0.5, o = {{}}) {{
  const s = Math.max(W / img.width, H / img.height) * z, iw = img.width * s, ih = img.height * s;
  const x = clamp(W / 2 - fx * iw, W - iw, 0), y = clamp(H / 2 - fy * ih, H - ih, 0);
  g.save(); g.globalAlpha = o.alpha ?? 1; g.drawImage(img, x, y, iw, ih); g.restore();
}}
function dim(g, top = 0.6, bottom = 0.75) {{
  g.save(); let gr = g.createLinearGradient(0, 0, 0, H * 0.48); gr.addColorStop(0, `rgba(0,4,10,${{top}})`); gr.addColorStop(0.55, `rgba(0,4,10,${{top * 0.6}})`); gr.addColorStop(1, 'rgba(0,0,0,0)'); g.fillStyle = gr; g.fillRect(0, 0, W, H * 0.48);
  gr = g.createLinearGradient(0, H * 0.5, 0, H); gr.addColorStop(0, 'rgba(0,0,0,0)'); gr.addColorStop(1, `rgba(0,4,10,${{bottom}})`); g.fillStyle = gr; g.fillRect(0, H * 0.5, W, H * 0.5); g.restore();
}}
function big(g, str, cx, cy, size, color, o = {{}}) {{
  const px = S.u * size, pop = o.pop ?? 1; if (pop <= 0) return;
  g.save(); g.translate(W * cx, H * cy); g.scale(pop, pop); g.globalAlpha = (o.alpha ?? 1) * Math.min(1, pop);
  setType(g, TYPE, o.role ?? 'display', px, {{ weight: o.weight ?? 900, track: o.track ?? 0.01 }}); g.textAlign = 'center'; g.textBaseline = 'middle';
  if (o.box) {{ const w = g.measureText(str).width; g.fillStyle = o.box; g.beginPath(); g.roundRect(-w / 2 - px * 0.45, -px * 0.62, w + px * 0.9, px * 1.2, px * 0.25); g.fill(); }}
  else {{ g.shadowColor = 'rgba(0,0,0,0.9)'; g.shadowBlur = px * 0.2; g.shadowOffsetY = px * 0.04; }}
  g.fillStyle = color; g.fillText(str, 0, px * 0.04); g.restore();
}}
// Titles over the pictures: [text, from, to, y, size, colour, kind]
const TITLES = {J(titles)};
function reel(g, k, t) {{
  g.fillStyle = '#020a12'; g.fillRect(0, 0, W, H);
  SHOTS.forEach(([key, a, b, z0, z1, fx0, fx1, fy0, fy1], i) => {{
    const first = i === 0, start = first ? a : a - XF; if (t < start || t >= b) return;
    const u = clamp((t - start) / (b - start)), e = EASE.inOut(u), alpha = first ? 1 : clamp((t - start) / XF);
    const hx = Math.sin(t * 0.9 + i) * 0.006, hy = Math.cos(t * 0.7 + i * 2) * 0.006;   // a slow drift, so the stills breathe like footage
    photo(g, PH[key], lerp(z0, z1, e), lerp(fx0, fx1, e) + hx, lerp(fy0, fy1, e) + hy, {{ alpha }});
  }});
  // a deep-water wash: the picture sinks toward blue as the story goes down
  g.save(); g.globalCompositeOperation = 'multiply'; g.fillStyle = `rgba(70,140,200,${{{getattr(S, 'WASH', 0.22)}}})`; g.fillRect(0, 0, W, H); g.restore();
  if (t >= END_AT) {{ g.fillStyle = `rgba(2,8,16,${{0.5 * clamp((t - END_AT) / 0.6)}})`; g.fillRect(0, 0, W, H); }}
  FLASHES.forEach(([a, d]) => {{ if (t >= a && t < a + d) {{ const k = (t - a) / d; g.fillStyle = `rgba(255,255,250,${{k < 0.12 ? k / 0.12 : Math.pow(1 - (k - 0.12) / 0.88, 1.6)}})`; g.fillRect(0, 0, W, H); }} }});
  dim(g, 0.85, 0.7);
  CLOCKS.forEach(([a, b, s0, r, y, sz, c]) => {{ if (t < a || t >= b) return;
    const sec = Math.floor(s0 + (t - a) * r), hh = Math.floor(sec / 3600), mm = Math.floor(sec / 60) % 60, ss = sec % 60;
    const str = String(hh).padStart(2, '0') + ':' + String(mm).padStart(2, '0') + ':' + String(ss).padStart(2, '0');
    big(g, str, CXc, y, sz, PALETTE[c], {{ pop: slam(t, a), alpha: clamp((b - t) / 0.15), track: 0.04 }}); }});
  TITLES.forEach(([s, a, b, y, size, col, kind]) => {{ if (t < a || t >= b) return; const out = clamp((b - t) / 0.2);
    if (kind === 'button') big(g, s, CXc, y, size, '#ffffff', {{ pop: popIn(t, a, 0.45) * (1 + 0.04 * Math.sin(Math.max(0, t - a - 0.5) * 6)), alpha: out, box: '#ff1f1f', weight: 800, track: 0.06 }});
    else big(g, s, CXc, y, size, PALETTE[col], {{ pop: kind === 'slam' ? slam(t, a) : popIn(t, a, 0.4), alpha: out, track: kind === 'track' ? 0.22 : 0.02, box: null }}); }});
}}
function overlay(g, t) {{
  const s = SUBS.find((r) => t >= r.at && t < r.to); if (!s) return;
  const a = clamp((t - s.at) / 0.1) * clamp((s.to - t) / 0.1), px = S.u * 0.046;
  g.save(); g.setTransform(1, 0, 0, 1, 0, 0); g.globalAlpha = a;
  setType(g, TYPE, 'text', px, {{ weight: 700, track: 0 }}); g.textAlign = 'center'; g.textBaseline = 'alphabetic';
  const lines = wrap(g, s.text, W * 0.74, true), lh = px * 1.28, y0 = H * 0.8 - (lines.length - 1) * lh / 2;
  const w = Math.max(...lines.map((l) => g.measureText(l).width));
  g.fillStyle = 'rgba(0,6,14,0.72)'; g.beginPath(); g.roundRect(W * CXc - w / 2 - px * 0.5, y0 - px * 1.1, w + px, lh * lines.length + px * 0.45, px * 0.35); g.fill();
  g.fillStyle = '#fff'; lines.forEach((ln, i) => g.fillText(ln, W * CXc, y0 + i * lh)); g.restore();
}}
// A low rising sweep (a designed sound in the spirit of the slowed-down hydrophone recordings, not the recording itself)
function sweep(ctx, out, t, gain, f0 = 38, f1 = 150, d = 1.6) {{
  [1, 2].forEach((h, j) => {{ const o = ctx.createOscillator(), v = ctx.createGain(); o.type = 'sine';
    o.frequency.setValueAtTime(f0 * h, t); o.frequency.exponentialRampToValueAtTime(f1 * h, t + d * 0.8);
    v.gain.setValueAtTime(0.0001, t); v.gain.exponentialRampToValueAtTime(gain / (j + 1), t + 0.2); v.gain.exponentialRampToValueAtTime(0.0001, t + d);
    o.connect(v).connect(out); o.start(t); o.stop(t + d + 0.05); }});
}}
function bell(ctx, out, t, gain) {{
  [[1, 1], [2.0, 0.6], [2.4, 0.5], [3.0, 0.35], [4.2, 0.25], [5.4, 0.15]].forEach(([m, a]) => {{ const o = ctx.createOscillator(), v = ctx.createGain(); o.type = 'sine';
    o.frequency.value = 196 * m; v.gain.setValueAtTime(0.0001, t); v.gain.exponentialRampToValueAtTime(gain * a, t + 0.01); v.gain.exponentialRampToValueAtTime(0.0001, t + 4.5 / m);
    o.connect(v).connect(out); o.start(t); o.stop(t + 5); }});
}}
function score(ctx, out) {{
  BELLS.forEach((t) => bell(ctx, wet(ctx, out, 0.6), t, 0.22));
  ambience(ctx, out, 0, DURATION, 'water', 0.05, 11);
  ambience(ctx, out, 0, DURATION, 'room', 0.05, 12);
  {J([[at(x[0])]+list(x[1:]) for x in getattr(S, 'SWEEPS', [])])}.forEach(([t, g, f0, f1, d]) => sweep(ctx, wet(ctx, out, 0.5), t, g, f0, f1, d));
}}

"""
a = tpl.index('// ============================== FILM ====='); b = tpl.index('// ============================== HELPERS (picture)')
open(os.path.join(film, 'film.html'), 'w').write(tpl[:a] + film_src + tpl[b:])
mix = {'duration': DURATION, 'out': 'audio/mix-v1.wav', 'layers': [{'file': 'audio/film.wav', 'at': 0.0, 'gain_db': 0, 'bus': 'music'}] +
       [{'file': f'audio/vo-t/VO{i+1}.wav', 'at': VT[i], 'gain_db': 0, 'bus': 'dialogue', 'pan': 0} for i in range(len(VT))]}
json.dump(mix, open(os.path.join(film, 'audio/mix.json'), 'w'), indent=1)
print('DURATION', DURATION, 'VT', VT)
