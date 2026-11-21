# Critique — draft-v2

1. **13.0–14.8 s · the hero year contradicts the voice.** The narration says "GTA Five came out in 2013", but the big year counter runs 2013 → 2026 and holds on **2026** under that line. The tile's own tag says "GTA V", so a first-time viewer reads "GTA V · 2026". The 2013→2026 idea belongs to the "Thirteen years later" ending (24 s). **Fix:** keep the big number on 2013 (let the small timeline bar fill to 2026 if you want), or drop the counter here and use it at 24 s.

2. **19.0–19.6 s · the transition looks broken.** The cut from the lifeguard tower to the aerial is a smeared pixel-stretch that lasts about half a second. Inside it, an empty grey rectangle (the bar chart before it fills) floats over the blur with no number or label. Then "UP TO 3M" appears, with the narration already saying "fifty-one million". It reads as a render fault. **Fix:** use a plain hard cut (or a short dissolve) at 19.06. Show the bar's frame and "UP TO" label from the first frame, and start the count at about 20M instead of 0, so the number reaches 51M while "fifty-one million" is spoken.

3. **0–6 s and throughout · the small type is too small for a phone.** The narration captions (about 14 px tall at this half-size render), the pink tags ("COUNTDOWN · GTA VI", "TRAILER 1 · DEC 2023", "FIRST WEEK · NEWZOO ESTIMATE"), "PS5 · XBOX SERIES X|S" and the "11 DAYS · NOV 19" end tag are all hard to read at Shorts viewing size. On the 4–6 s map, the "MIAMI" label and the tiny date pin are the only content, on a pale, mostly empty frame. **Fix:** scale the captions and tags up by about 1.4x, and enlarge the map labels. The end tag "11 DAYS · NOV 19" should be at least half the height of "VICE CITY".

Other notes: the opening countdown (99 → 11) and the ending callback ("11 DAYS · NOV 19") tie together well. The cut to "WORLD RECORD" at 11.1 s lands right on "A world record." Audio is clean: -13.8 LUFS, true peak -3.3 dBFS, no silences, no scene flagged. The 24–30.5 s bridge is one photo held for 6.5 s, but the text changes keep it alive.

Verdict: FIX
Red items:
- 19.0–19.6 s smeared transition with an empty grey box (reads as a broken render)
- 13–14.8 s big year lands on "2026" while the narration says 2013 for GTA V
Polish: bigger tags and captions; a little more detail on the empty map at 4–5 s; a "51M" landing timed to the word "fifty-one"; give the 24–30 s bridge a slow push-in to add variety.
Evidence: review/qc-draft-v2/sheet.jpg (1 fps, 0–30 s); strips strip-0s.jpg, strip-13s.jpg, strip-18.6s.jpg; report.txt (cuts at 6.917 and 11.125; 8 scenes, none flagged; I -13.8 LUFS, LRA 1.2, peak -3.3 dBFS; no black, freeze, duplicates or pops).
