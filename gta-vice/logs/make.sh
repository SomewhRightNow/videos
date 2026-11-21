#!/bin/bash
# scene png -> HD character image with the player's real face. usage: make.sh <scene.png> <player_photo> <out.png>
set -e; PY=/home/user/.sdvenv/bin/python; D=/home/user/Filmler/gta-vice/logs; t=$(mktemp -d)
$PY $D/upscale.py "$1" $t/up.png >/dev/null 2>&1
PASSES=${PASSES:-3} $PY $D/swap2.py $t/up.png "$2" $t/sw.png 1.0 0.0 2>&1 | grep -q "^ok"
$PY $D/restore_hd.py $t/sw.png $t/rs.png codeformer ${FID:-0.85} 2>&1 | grep -q "^ok"
python3 -c "
from PIL import Image, ImageFilter
im=Image.open('$t/rs.png').convert('RGB'); im=im.filter(ImageFilter.UnsharpMask(radius=1.6,percent=55,threshold=2)); im.save('$3')"
rm -rf $t; echo done "$3"
