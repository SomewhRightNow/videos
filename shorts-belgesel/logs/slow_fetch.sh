#!/bin/bash
# polite retry: one file at a time, long pauses, for Wikimedia's rate limit
cd "$(dirname "$0")/.."
jobs="sylbaris:11 sylbaris:8 sp-ruins:13 sp-ruins:14 sp-ruins:15 sp-ruins:16 sp-ruins:17 sp-ruins:23 pelee:12 pelee:13 pelee:14 pelee:17 v-pelee:1"
for round in 1 2; do
  for j in $jobs; do
    d=${j%%:*}; n=${j##*:}; dest=assets/img; [ "$d" = v-pelee ] && dest=assets/video
    grep -q "^$j$" logs/slow_done.txt 2>/dev/null && continue
    out=$(python3 tools/asset_search.py fetch --results research/$d/results.json --pick $n --dest $dest 2>&1)
    echo "$j: $out" | head -1 >> logs/slow_fetch.log
    echo "$out" | grep -q "failed" || echo "$j" >> logs/slow_done.txt
    sleep 45
  done
done
echo DONE >> logs/slow_fetch.log
