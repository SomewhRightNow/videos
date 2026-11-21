#!/bin/bash
# EN narration: Kokoro am_michael, then trim leading/trailing silence
cd /home/user/Filmler/neymar
PY=~/.cinecode/kokoro/venv/bin/python
i=0
while IFS= read -r line; do
  i=$((i+1))
  [ -n "$ONLY" ] && [[ ",$ONLY," != *",$i,"* ]] && continue
  $PY logs/kokoro_tts.py am_michael 1.0 audio/vo/VO$i.wav "$line" >/dev/null 2>&1 </dev/null
  ffmpeg -nostdin -y -loglevel error -i audio/vo/VO$i.wav -af "silenceremove=start_periods=1:start_threshold=-45dB,areverse,silenceremove=start_periods=1:start_threshold=-45dB,areverse" -ar 24000 audio/vo-t/VO$i.wav
done < logs/lines.txt
echo done
