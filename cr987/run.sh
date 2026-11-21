#!/bin/bash
# usage: ./run.sh "Output name.mp4"   (cfg.json must be filled: src, t_goal, t_frz, src_end, n, line)
set -e; cd "$(dirname "$0")"
OUTN="$1"; rm -f out/*.mp4
python3 film.py full > logs/render.log 2>&1
TG=$(python3 -c "import json;print(json.load(open('cfg.json'))['t_goal'])")
T=$(python3 -c "import json;c=json.load(open('cfg.json'));print(round(c['t_frz']+1.2+(c['src_end']-c['t_frz'])+2.8,3))")
OFF=$(python3 -c "print(round(42.53-$TG,3))")
ffmpeg -nostdin -loglevel error -y -ss $OFF -t $T -i audio/fsm-team-moonlit.mp3 -af "afade=t=out:st=$(python3 -c "print($T-1.8)"):d=1.8,loudnorm=I=-14:TP=-1.5:LRA=11" -ar 48000 -ac 2 audio/mix.wav
find out -name 'part*.mp4' -delete
python3 film.py deliver "$OUTN"; rm -f out/video.mp4
ffprobe -v error -show_entries format=duration -of csv=p=0 "$OUTN"
