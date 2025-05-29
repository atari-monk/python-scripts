import math
import pyaudio
import struct
import time
from collections import defaultdict
from pathlib import Path
from typing import Optional

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
    data = defaultdict(dict)
    
    lines = []
    if log_file_path.exists():
        with open(log_file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    
    current_date = None
    for line in lines:
        line = line.rstrip('\n')
        if not line.strip():
            continue
        if not line.startswith(' '):
            current_date = line.rstrip(':')
            data[current_date] = {}
        else:
            try:
                time_part, msg_part = line.strip().split(': ', 1)
                if current_date is not None:
                    data[current_date][time_part] = msg_part
            except ValueError:
                pass
    
    data[date][current_time] = message.lower()
    
    with open(log_file_path, 'w', encoding='utf-8') as f:
        for d in sorted(data.keys()):
            f.write(f"{d}:\n")
            for t in sorted(data[d].keys()):
                f.write(f"  {t}: {data[d][t]}\n")

def show_todays_records(log_file_path: Path) -> None:
    if not log_file_path.exists():
        print("No records found for today.")
        return
    
    today = time.strftime('%Y-%m-%d')
    with open(log_file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    print(f"\n📅 Today's Focus Records ({today}):")
    found = False
    current_date = None
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
        if not line.startswith(' '):
            current_date = line.rstrip(':')
            if current_date == today:
                found = True
            else:
                current_date = None
        elif current_date is not None:
            print(f"  {line}")
    
    if not found:
        print("No records found for today.")

def ask_check_in(log_file_path: Path) -> Optional[str]:
    play_tone(440.0, 0.3)
    print("\n🔔 Focus Check-In Menu")
    print("1: 🚀 In Flow")
    print("2: 😐 Neutral")
    print("3: 😩 Struggling")
    print("4: 🤯 Overwhelmed")
    print("5: 🛑 Need Break")
    print("6: 📊 View Today's Records")
    print("0: Skip (No Log)")
    choice = input("Select an option (1-6) or 0 to skip: ").strip()
    
    states = {
        "1": "🚀 in flow",
        "2": "😐 neutral",
        "3": "😩 struggling",
        "4": "🤯 overwhelmed",
        "5": "🛑 need break"
    }
    
    if choice == "0":
        print("Skipping log entry.\n")
        return None
    elif choice == "6":
        show_todays_records(log_file_path)
        return None
    elif choice in states:
        note = input("Add optional note (or press Enter): ").strip()
        message = states[choice] + (f" - {note.lower()}" if note else "")
        log_attention_yaml(log_file_path, message)
        play_tone(880.0, 0.3)
        print(f"Logged: {message}\n")
        return message
    else:
        print("Invalid choice. Skipping.\n")
        return None

def periodic_check_in(log_file: Path, interval_min: int) -> None:
    interval_sec = interval_min * 60
    try:
        while True:
            start_time = time.time()
            ask_check_in(log_file)
            
            remaining = interval_sec
            while remaining > 0:
                mins, secs = divmod(remaining, 60)
                if mins % 5 == 0 or remaining == interval_sec or remaining < 60:
                    print(f"⏳ Next check-in in: {mins}m {secs}s")
                time.sleep(1)
                remaining = interval_sec - (time.time() - start_time)
                
    except KeyboardInterrupt:
        print("\n⏹️ Check-ins stopped.")

def main(log_file_path: Path = Path(r"C:\atari-monk\code\apps-data-store\attention_log.yaml"), interval_min: int = 15) -> None:
    print(f"\n🎯 Goal: Deep Focus")
    print(f"⏰ You'll be prompted every {interval_min} minutes")
    print("Press Ctrl+C to stop at any time.\n")
    periodic_check_in(log_file_path, interval_min)

if __name__ == "__main__":
    main()