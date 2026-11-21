#!/bin/bash
# Two-way sync of the shared workspace (rules, notes, code) with GitHub branch "workspace".
# pull: bring in work done on any other account. push: publish local changes. Media is never synced (.gitignore whitelist).
# Merge rule: OPERASYON.md / HANDOFF.md / CLAUDE.md use union merge, so lines added on both sides are both kept.
R=https://github.com/SomewhRightNow/videos; D=/home/user/Filmler; cd "$D" 2>/dev/null || exit 0
LOCK=/tmp/srn_sync.lock; exec 9>$LOCK; flock -w 60 9 || exit 0
git rev-parse --git-dir >/dev/null 2>&1 || exit 0
git remote get-url origin >/dev/null 2>&1 || git remote add origin $R
commit_local() { git add -A >/dev/null 2>&1; git diff --cached --quiet || git commit -q -m "sync: $(hostname) $(date -u +%FT%TZ)" >/dev/null 2>&1; }
pull() {
  git fetch -q origin workspace 2>/dev/null || return 0
  commit_local
  git merge -q --no-edit -X ours origin/workspace >/dev/null 2>&1 || { git merge --abort 2>/dev/null; git merge -q --no-edit -X theirs origin/workspace >/dev/null 2>&1; }
  # install rules for Claude in this container
  mkdir -p ~/.claude; grep -q "@/home/user/Filmler/CLAUDE.md" ~/.claude/CLAUDE.md 2>/dev/null || printf '@/home/user/Filmler/CLAUDE.md\n' > ~/.claude/CLAUDE.md
  FD=/mnt/skills/examples/canvas-design/canvas-fonts; [ -d "$FD" ] || { mkdir -p "$FD" 2>/dev/null && cp -n "$D"/fonts/* "$FD"/ 2>/dev/null; }
}
push() {
  pull
  git diff --quiet origin/workspace HEAD 2>/dev/null && return 0
  for i in 1 2 3; do git push -q origin HEAD:workspace >/dev/null 2>&1 && return 0; sleep 3; pull; done
}
case "$1" in pull) pull;; push) push;; *) echo "usage: srn_sync.sh pull|push";; esac
exit 0
