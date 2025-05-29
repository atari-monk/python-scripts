from pathlib import Path
import yaml
import datetime
import time
from pyaudio import PyAudio
import numpy as np
from typing import Dict, Any
import threading
import queue

def generate_beep(freq: float = 880, duration: float = 0.08) -> bytes:
    fs = 44100
    samples = (np.sin(2 * np.pi * np.arange(int(fs * duration)) * freq / fs)).astype(np.float32)
    return samples.tobytes()

class Beeper:
    def __init__(self) -> None:
        self.p = PyAudio()
        self.stream = self.p.open(format=self.p.get_format_from_width(4),
                                  channels=1,
                                  rate=44100,
                                  output=True)
        self.beep_queue: queue.Queue[bytes] = queue.Queue()
        self.running = True
        self.thread = threading.Thread(target=self._run)
        self.thread.start()

    def _run(self) -> None:
        while self.running or not self.beep_queue.empty():
            try:
                beep: bytes = self.beep_queue.get(timeout=0.1)
                self.stream.write(beep)
            except queue.Empty:
                continue

    def beep(self, freq: float = 880, duration: float = 0.2) -> None:
        self.beep_queue.put(generate_beep(freq=freq, duration=duration))

    def triple_beep(self) -> None:
        for _ in range(3):
            self.beep()
            time.sleep(1.0)

    def startup_test(self) -> None:
        print("testing 3-beep startup signal...")
        self.triple_beep()

    def stop(self) -> None:
        self.running = False
        self.thread.join()
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()

file_path = Path(r'c:\atari-monk\code\apps-data-store\stuff_done_log.yaml')

def load_data() -> Dict[str, Any]:
    try:
        with open(file_path, 'r') as f:
            return yaml.safe_load(f) or {}
    except FileNotFoundError:
        return {}

def save_data(data: Dict[str, Any]) -> None:
    with open(file_path, 'w') as f:
        yaml.dump(data, f, sort_keys=False, default_flow_style=False)

def get_current_date() -> str:
    return datetime.datetime.now().strftime('%Y-%m-%d')

def get_current_time() -> str:
    return datetime.datetime.now().strftime('%H:%M')

def add_task(data: Dict[str, Any], date: str, start_time: str, end_time: str, task: str) -> None:
    if date not in data:
        data[date] = []
    data[date].append({
        'start': start_time,
        'task': task,
        'end': end_time
    })

def task_loop(beeper: Beeper) -> None:
    data = load_data()
    current_date = get_current_date()

    while True:
        print("\n--- new task ---")
        task: str = input("enter task name (max 200 chars): ").lower()[:200]
        print("press enter to start task...")
        input()

        start_time = get_current_time()
        beeper.beep()
        print("task started. press enter to end...")

        task_start = time.time()
        last_beep = task_start

        stop_event = threading.Event()

        def wait_for_enter() -> None:
            input()
            stop_event.set()

        input_thread = threading.Thread(target=wait_for_enter)
        input_thread.start()

        while not stop_event.is_set():
            current_time = time.time()
            if current_time - last_beep >= 900:
                beeper.triple_beep()
                last_beep = current_time
            time.sleep(0.1)

        end_time = get_current_time()
        beeper.beep()

        add_task(data, current_date, start_time, end_time, task)
        save_data(data)

        while True:
            choice = input("add another task? (y/n): ").strip().lower()
            if choice in ['y', 'n']:
                break
        if choice == 'n':
            break

def main() -> None:
    beeper = Beeper()
    beeper.startup_test()
    try:
        task_loop(beeper)
    except KeyboardInterrupt:
        print("\nscript interrupted. data saved.")
    finally:
        beeper.stop()

if __name__ == "__main__":
    try:
        main()
    except ImportError as e:
        print(f"missing required library: {e.name}. please install it first.")