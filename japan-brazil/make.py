# usage: python3 make.py tts|probe|full  — lines come from result.json["lines"]
import json, subprocess, sys, os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
R = json.load(open('result.json')); VOICE = 'am_echo'
if sys.argv[1] == 'tts':
    open('logs/lines.txt', 'w').write('\n'.join(R['lines']) + '\n')
    for i, l in enumerate(R['lines'], 1):
        subprocess.run([os.path.expanduser('~/.cinecode/kokoro/venv/bin/python'), 'logs/kokoro_tts.py', VOICE, '1.15', f'audio/vo/VO{i}.wav', l], capture_output=True)
        subprocess.run(['ffmpeg', '-nostdin', '-y', '-loglevel', 'error', '-i', f'audio/vo/VO{i}.wav', '-af', 'silenceremove=start_periods=1:start_threshold=-45dB,areverse,silenceremove=start_periods=1:start_threshold=-45dB,areverse', f'audio/vo-t/VO{i}.wav'])
    print('tts ok')
