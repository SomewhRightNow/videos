import os, random
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageChops
os.chdir(os.path.dirname(os.path.abspath(__file__)))
W, H = 2560, 1440
F = '/home/user/Filmler/fonts/'
fB = lambda s: ImageFont.truetype(F + 'BigShoulders-Bold.ttf', s)
fO = lambda s: ImageFont.truetype(F + 'Outfit-Bold.ttf', s)
RED=(190,14,30); RED2=(90,4,12); GOLD=(250,200,30); GOLD2=(120,80,0); GREEN=(0,120,60)
def grad(c1,c2,w,h,horiz=False):
    g=Image.new('RGB',(w,h)); d=ImageDraw.Draw(g)
    n=w if horiz else h
    for i in range(n):
        u=i/(n-1); c=tuple(int(c1[k]+(c2[k]-c1[k])*u) for k in range(3))
        d.line([(i,0),(i,h)] if horiz else [(0,i),(w,i)],fill=c)
    return g
# background: radial-ish gradients both halves
L=grad(RED,RED2,W,H,True); R=grad(GOLD2,(235,170,20),W,H,True)
mask=Image.new('L',(W,H),0); ImageDraw.Draw(mask).polygon([(1380,0),(W,0),(W,H),(1180,H)],fill=255)
bg=Image.composite(R,L,mask)
# vignette + light streaks
v=Image.new('L',(W,H),0); ImageDraw.Draw(v).ellipse([-600,-500,W+600,H+500],fill=255); v=v.filter(ImageFilter.GaussianBlur(260))
bg=Image.composite(bg,Image.new('RGB',(W,H),(8,6,10)),v)
# noise grain
random.seed(1); n=Image.effect_noise((W,H),18).convert('RGB'); bg=ImageChops.overlay(bg,Image.blend(Image.new('RGB',(W,H),(128,128,128)),n,0.25))
d=ImageDraw.Draw(bg)
# white divider stripe
d.polygon([(1368,0),(1392,0),(1192,H),(1168,H)],fill=(255,255,255))
# soft glow behind players
def glow(cut,col,rad=40,a=230):
    al=cut.getchannel('A').filter(ImageFilter.MaxFilter(9)).filter(ImageFilter.GaussianBlur(rad))
    g=Image.new('RGBA',cut.size,col+(0,)); g.putalpha(al.point(lambda x:min(255,int(x*a/255)))); return g
def rim(cut,col=(255,255,255),w=7):
    al=cut.getchannel('A'); big=al.filter(ImageFilter.MaxFilter(w*2+1)); r=Image.new('RGBA',cut.size,col+(255,)); r.putalpha(big); return r
def place(name,h,x,y,gcol):
    c=Image.open(name).convert('RGBA'); s=h/c.height; c=c.resize((int(c.width*s),h),Image.LANCZOS)
    c=Image.merge('RGBA',[*c.convert('RGB').filter(ImageFilter.UnsharpMask(2,80,2)).split(),c.getchannel('A')])
    for lay in (glow(c,gcol,70,200),rim(c)):
        bg.paste(lay,(x,y),lay)
    bg.paste(c,(x,y),c); return c.width
# Nico left (mirror so he looks toward centre? he already looks right). Inaki right.
place('nico_cut.png',1500,140,40,(255,90,60))
ic=Image.open('inaki_cut.png'); 
place('inaki_cut.png',1450,W-1400,90,(255,230,120))
d=ImageDraw.Draw(bg)
# bottom dark band for text
band=Image.new('L',(1,H)); band.putdata([0 if i<H-560 else int(235*((i-(H-560))/560)**0.8) for i in range(H)])
bg.paste(Image.new('RGB',(W,H),(6,6,10)),(0,0),band.resize((W,H))); d=ImageDraw.Draw(bg)
def ct(y,s,f,fill,st=10,x=None):
    w=d.textlength(s,font=f); xx=(W-w)/2 if x is None else x
    sh=Image.new('RGBA',(W,H),(0,0,0,0)); ImageDraw.Draw(sh).text((xx+8,y+10),s,font=f,fill=(0,0,0,200),stroke_width=st,stroke_fill=(0,0,0,200))
    bg.paste(sh.filter(ImageFilter.GaussianBlur(10)),(0,0),sh.filter(ImageFilter.GaussianBlur(10)))
    ImageDraw.Draw(bg).text((xx,y),s,font=f,fill=fill,stroke_width=st,stroke_fill=(0,0,0))
ct(H-500,'SAME PARENTS.',fB(250),(255,255,255),10)
ct(H-270,'DIFFERENT COUNTRIES.',fB(230),GOLD,10)
d=ImageDraw.Draw(bg)
# country pills
def pill(cx,y,s,fill,tc):
    f=fB(92); w=d.textlength(s,font=f); d.rounded_rectangle([cx-w/2-40,y,cx+w/2+40,y+120],30,fill=fill,outline=(255,255,255),width=6); d.text((cx-w/2,y+6),s,font=f,fill=tc)
pill(330,90,'SPAIN',RED,(255,215,40)); pill(W-330,90,'GHANA',(10,10,12),GOLD)
# centre WHY? badge
cx,cy=1235,540; r=165
d.ellipse([cx-r-10,cy-r-10,cx+r+10,cy+r+10],fill=(255,255,255)); d.ellipse([cx-r,cy-r,cx+r,cy+r],fill=(12,12,16))
f=fB(130); w=d.textlength('WHY?',font=f); d.text((cx-w/2,cy-86),'WHY?',font=f,fill=GOLD)
bg.save('thumbnail_2560.jpg',quality=95); bg.resize((1280,720),Image.LANCZOS).save('thumbnail_1280.jpg',quality=93)
bg.resize((320,180),Image.LANCZOS).save('small_chk.png')
