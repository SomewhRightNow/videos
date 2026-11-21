#!/bin/bash
# usage: ./sheet.sh src/clip.mp4 [start] [dur] [fps]  -> logs/sheet.jpg
ffmpeg -nostdin -loglevel error -y -ss ${2:-0} -t ${3:-30} -i "$1" -vf "fps=${4:-2},scale=200:-2,drawtext=text='%{pts\:hms}':x=4:y=4:fontcolor=yellow:fontsize=14,tile=10x6" -frames:v 1 "$(dirname "$0")/logs/sheet.jpg"
