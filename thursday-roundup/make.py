# Build narration lines from data.json and synthesize them (voice changes per video).
import json, subprocess, os
D = json.load(open('data.json'))
NUM = ['nil', 'one', 'two', 'three', 'four', 'five', 'six', 'seven']
def sp(score): a, b = [int(x) for x in score.replace('–', '-').split('-')]; return NUM[a], NUM[b]
t1, t2 = sp(D['early'][0]['score']); a1, a2 = sp(D['early'][1]['score'])
lines = [
 "Thursday night in the Nations League. Here's what you missed, and what's next.",
 f"Full time: Türkiye {t1}, Belgium {t2}.",
 f"Armenia {a1}, Cyprus {a2}.",
 f"Man of the match: {D['motm_spoken']}.",
 "And later tonight, the big games kick off.",
 "Italy against France at San Siro. England host Croatia at Wembley. And Czechia take on Spain.",
 "Plus Albania against Finland, Montenegro against Latvia, and San Marino against Belarus.",
 "Italy or France? Drop your score below. Results right here on this channel.",
]
open('logs/lines.txt', 'w').write('\n'.join(lines) + '\n')
os.makedirs('audio/vo', exist_ok=True); os.makedirs('audio/vo-t', exist_ok=True)
for i, l in enumerate(lines, 1):
    subprocess.run([os.path.expanduser('~/.cinecode/kokoro/venv/bin/python'), 'logs/kokoro_tts.py', D.get('voice', 'bm_daniel'), '1.12', f'audio/vo/VO{i}.wav', l], stdin=subprocess.DEVNULL, capture_output=True)
    subprocess.run(['ffmpeg', '-nostdin', '-y', '-loglevel', 'error', '-i', f'audio/vo/VO{i}.wav', '-af', 'silenceremove=start_periods=1:start_threshold=-45dB,areverse,silenceremove=start_periods=1:start_threshold=-45dB,areverse', '-ar', '48000', f'audio/vo-t/VO{i}.wav'])
print('\n'.join(lines))
