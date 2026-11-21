#!/bin/bash
# low-fps God's Eye View frames -> 30 fps (motion blend), 1920x1080
cd /home/user/Filmler/neymar/src/gev
for s in "$@"; do
  f=6; [ "$s" = santos ] && f=4
  mkdir -p ${s}_30
  ffmpeg -nostdin -y -loglevel error -framerate $f -i $s/f_%04d.jpg -vf "scale=1920:1080:flags=lanczos,minterpolate=fps=30:mi_mode=blend" -q:v 2 ${s}_30/f_%04d.jpg
  echo $s $(ls ${s}_30 | wc -l)
done
