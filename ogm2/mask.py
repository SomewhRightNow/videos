import cv2, numpy as np
fs=[cv2.imread(f'src/fa/f_{k:04d}.jpg') for k in range(1625,1790,3)]
A=np.stack(fs).astype(np.float32); std=A.std(0).mean(2); med=np.median(A,0).astype(np.uint8)
hsv=cv2.cvtColor(med,cv2.COLOR_BGR2HSV); lum=cv2.cvtColor(med,cv2.COLOR_BGR2GRAY); h=hsv[...,0]; s=hsv[...,1]
white=(lum>185)&(s<80); black=lum<55; flag=((s>90)&((h<10)|(h>165)))|((s>50)&(h>92)&(h<128)); yb=(s>70)&(h>=8)&(h<=32)&(std<12); green=(s>160)&(lum<130)&(std<9)
m=((std<18)&(white|black|flag|green|yb)).astype(np.uint8)*255
R=np.zeros_like(m); R[600:1080,50:470]=1; R[1035:1080,440:650]=1; m=m*R
n,lab,st,_=cv2.connectedComponentsWithStats(m); keep=np.zeros_like(m)
for i in range(1,n):
    if st[i,4]>=6: keep[lab==i]=255
m=cv2.dilate(keep,np.ones((5,5),np.uint8),iterations=2); cv2.imwrite('logs/mask.png',m)
for k,nm in ((1500,'inp2'),(1100,'inp3'),(700,'inp4')):
    t=cv2.imread(f'src/fa/f_{k:04d}.jpg'); o=cv2.inpaint(t,m,4,cv2.INPAINT_TELEA); cv2.imwrite(f'logs/{nm}.jpg',np.hstack([t[560:1080,0:700],o[560:1080,0:700]]))
