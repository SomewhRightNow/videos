import sys, subprocess
from PIL import Image, ImageDraw
f, name, a, b, step = sys.argv[1], sys.argv[2], float(sys.argv[3]), float(sys.argv[4]), float(sys.argv[5])
ts = []; t = a
while t <= b + 1e-6: ts.append(round(t, 2)); t += step
ims = []
for k, t in enumerate(ts):
    subprocess.run(['ffmpeg','-nostdin','-y','-loglevel','error','-ss',str(t),'-i',f,'-frames:v','1','-vf','scale=320:-2',f'out/_d{k}.jpg'])
    im = Image.open(f'out/_d{k}.jpg').convert('RGB'); ImageDraw.Draw(im).text((4,4), f'{t:.1f}', fill='yellow'); ims.append(im)
w, h = 320, ims[0].height; cols = 8; S = Image.new('RGB', (w * cols, h * ((len(ims) + cols - 1) // cols)))
for k, im in enumerate(ims): S.paste(im.resize((w, h)), ((k % cols) * w, (k // cols) * h))
S.save(f'out/dense_{name}.jpg')
