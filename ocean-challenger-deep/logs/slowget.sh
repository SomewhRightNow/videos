for spec in "bathyscaphe Trieste:9" "bathyscaphe Trieste:0" "bathyscaphe Trieste:11" "Challenger Deep:12" "Challenger Deep:9" "Challenger Deep:2" "Challenger Deep:7" "bathyscaphe Trieste:5"; do
  python3 logs/cand.py research/wm.json "$spec" >/dev/null 2>&1; sleep 25; done
find research/cand -size 0 -delete; ls research/cand
