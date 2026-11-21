#!/bin/bash
# SessionStart: print shared state so Claude starts with the latest status and conversation from any account.
D=/home/user/Filmler; [ -d "$D" ] || exit 0
echo "=== ORTAK ÇALIŞMA ALANI (workspace dalı, tüm hesaplar) ==="
echo "--- HANDOFF.md (son durum) ---"; tail -n 60 "$D/HANDOFF.md" 2>/dev/null
L=$(ls "$D"/konusmalar/*.md 2>/dev/null | sort | tail -1)
[ -n "$L" ] && { echo "--- Son konuşmalar ($(basename "$L")) ---"; tail -n 120 "$L"; }
echo "(Tüm konuşmalar: $D/konusmalar/, kurallar: $D/CLAUDE.md, kayıt: $D/OPERASYON.md)"
exit 0
