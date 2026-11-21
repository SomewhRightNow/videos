#!/bin/bash
cd /home/user/Filmler/gta-vice; export HF_HOME=/home/user/.hf HF_HUB_OFFLINE=1
for p in ronaldo mbappe vini kane haaland; do
  pr=$(python3 -c "import json;print(json.load(open('logs/prompts2.json'))['$p'])")
  /home/user/.sdvenv/bin/python logs/scene.py "$pr" scene/t_$p 301,302,303,304,305,306,307,308 576 768 2>&1 | grep -E "^[0-9]+ " | tr '\n' ' '; echo " $p done"
done
echo ALLDONE
