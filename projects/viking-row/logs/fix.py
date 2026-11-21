import sys; a,b=float(sys.argv[1]),float(sys.argv[2]); sys.argv=['film.py','x']
sys.path.insert(0,'/home/user/Filmler/viking-row')
import film as F
F.G.render_range((int(a*F.FPS),int(b*F.FPS),'out/fix.mp4'))
