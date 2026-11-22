#!/bin/bash
# SessionStart: make this container identical to the other account's: workspace, rules, skills, AI tools (background).
D=/home/user/Filmler
[ -d $D/.git ] || git clone -q -b workspace --single-branch https://github.com/SomewhRightNow/videos $D
bash $D/_sync/srn_sync.sh pull 2>/dev/null
mkdir -p ~/.claude/skills; [ -d ~/.claude/skills/cinematic-film ] || cp -r $D/_skills/cinematic-film ~/.claude/skills/ 2>/dev/null
[ -d ~/.claude/skills/cinecode ] || git clone -q https://github.com/sarpstar/cinecode ~/.claude/skills/cinecode 2>/dev/null
# base tools (Kokoro voice, ffmpeg, yt-dlp) and AI image tools: install once, in background so the session starts fast
[ -f ~/.cinecode/kokoro/voices-v1.0.bin ] || (nohup bash $D/setup.sh > /tmp/srn_setup.log 2>&1 &)
[ -f /home/user/.yolo/sam_vit_b.pth ] || (nohup bash $D/setup_ml.sh > /tmp/srn_setup_ml.log 2>&1 &)
# reference repos the user added (21.11): cloned in background
(mkdir -p $D/_refs; cd $D/_refs; for r in OpenMontageInc/openmontage lemomo-ai/lemo-opuscar JuneYaooo/rea-video kajisho5/ffmpeg-skill mvanhorn/last30days-skill krillinai/OpenCreator; do n=$(echo ${r#*/} | tr A-Z a-z); [ -d "$n" ] || git clone -q --depth 1 https://github.com/$r $n 2>/dev/null; done) >/dev/null 2>&1 &
(sleep 60; [ -d ~/.claude/skills/last30days ] || cp -r $D/_refs/last30days-skill/skills/last30days ~/.claude/skills/ 2>/dev/null) >/dev/null 2>&1 &
bash $D/_sync/context.sh
