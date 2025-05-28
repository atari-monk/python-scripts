import math
from pathlib import Path
import time
import struct
import pyaudio
from collections import defaultdict
from typing import DefaultDict

def play_tone(frequency: float, duration: float) -> None:
    sample_rate = 44100
    amplitude = 0.5
    num_samples = int(sample_rate * duration)

    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paFloat32, channels=1, rate=sample_rate, output=True)

    samples = (amplitude * math.sin(2 * math.pi * frequency * (i / sample_rate)) for i in range(num_samples))
    samples = b''.join(struct.pack('f', s) for s in samples)

    stream.write(samples)
    stream.stop_stream()
    stream.close()
    p.terminate()

def log_attention_yaml(log_file_path: Path, message: str) -> None:
    timestamp = time.strftime('%Y-%m-%d %H:%M')
    date, current_time = timestamp.split(' ')

    data: DefaultDict[str, dict[str, str]] = defaultdict(dict)

    if log_file_path.exists():
        with open(log_file_path, 'r') as f:
            lines = f.readlines()
        current_date = None
        for line in lines:
            line = line.rstrip('\n')
            if not line.strip():
                continue
            if not line.startswith(' '):  # date line
                current_date = line.rstrip(':')
                data[current_date] = {}
            else:
                try:
                    time_part, msg_part = line.strip().split(': ', 1)
                    if current_date is not None:
                        data[current_date][time_part] = msg_part
                except ValueError:
                    pass  # ignore malformed lines

    data[date][current_time] = message

    with open(log_file_path, 'w') as f:
        for d in sorted(data.keys()):
            f.write(f"{d}:\n")
            for t in sorted(data[d].keys()):
                f.write(f"  {t}: {data[d][t]}\n")

def ask_check_in(goal: str, log_file_path: Path) -> None:
    play_tone(440.0, 0.3)
    print("\n🔔 How is it going? Please type a quick reflection (or just press Enter):")
    response = input("> ").strip()
    if not response:
        response = "(No input)"
    log_attention_yaml(log_file_path, response)
    play_tone(880.0, 0.3)
    print(f"Keep going! Remember your goal: {goal}\n")

def periodic_check_in(goal: str, log_file: str, interval_sec: int) -> None:
    try:
        while True:
            time.sleep(interval_sec)
            ask_check_in(goal, log_file)
    except KeyboardInterrupt:
        print("\n⏹️ Stopping check-ins. Good job staying focused!")

def main(goal: str, log_file_path: Path = Path(r"C:\atari-monk\code\apps-data-store\attention_log.yaml"), interval_min: int = 15) -> None:
    print(f"\n🎯 Goal: {goal}")
    print(f"🕒 You will be prompted every {interval_min} minutes to check in.\nPress Ctrl+C to stop at any time.\n")
    ask_check_in(goal, log_file_path)
    periodic_check_in(goal, log_file_path, interval_min * 60)

if __name__ == "__main__":
    import sys
    user_goal = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else "Deep focus"
    main(user_goal)
