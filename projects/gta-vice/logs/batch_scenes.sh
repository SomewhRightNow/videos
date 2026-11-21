#!/bin/bash
cd /home/user/Filmler/gta-vice; export HF_HOME=/home/user/.hf HF_HUB_OFFLINE=1
for p in ronaldo messi mbappe yamal vini kane arda; do
  pr=$(python3 -c "import json;print(json.load(open('logs/prompts.json'))['$p'])")
  /home/user/.sdvenv/bin/python logs/scene.py "$pr" scene/s_$p 101,102,103,104,105,106,107,108 576 768 2>&1 | grep -E "^[0-9]+ " | tr '\n' ' '; echo " $p done"
done
echo ALLDONE
