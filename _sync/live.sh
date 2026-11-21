#!/bin/bash
# Runs before every user message: pull the other account's latest work and show what changed (new rules/notes/chat lines).
D=/home/user/Filmler; cd "$D" 2>/dev/null || exit 0
A=$(git rev-parse HEAD 2>/dev/null)
timeout 40 bash "$D/_sync/srn_sync.sh" pull >/dev/null 2>&1
B=$(git rev-parse HEAD 2>/dev/null)
[ "$A" = "$B" ] && exit 0
echo "=== DİĞER HESAPTAN YENİ DEĞİŞİKLİK (otomatik senkron) ==="
git diff --stat "$A" "$B" -- . ':(exclude)konusmalar' 2>/dev/null | tail -15
for f in CLAUDE.md HANDOFF.md; do git diff "$A" "$B" -- "$f" 2>/dev/null | grep '^+[^+]' | head -20; done
echo "--- yeni konuşma satırları ---"
git diff "$A" "$B" -- konusmalar 2>/dev/null | grep '^+[^+]' | cut -c2- | tail -40
exit 0
