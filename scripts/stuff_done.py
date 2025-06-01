from pathlib import Path
import yaml
import datetime
from pyaudio import PyAudio
import numpy as np
import threading
import queue
import sys

def generate_sound_wave(frequency=880, duration=0.08):
    sample_rate = 44100
    samples = np.sin(2 * np.pi * np.arange(int(sample_rate * duration)) * frequency / sample_rate)
    return samples.astype(np.float32).tobytes()

class SoundNotifier:
    def setup_audio(self):
        audio = PyAudio()
        stream = audio.open(
            format=audio.get_format_from_width(4),
            channels=1,
            rate=44100,
            output=True
        )
        return audio, stream

    def __init__(self):
        self.audio, self.stream = self.setup_audio()
        self.sound_queue = queue.Queue()
        self.active = True
        self.worker = threading.Thread(target=self.process_queue)
        self.worker.start()

    def process_queue(self):
        while self.active or not self.sound_queue.empty():
            try:
                sound = self.sound_queue.get(timeout=0.1)
                self.stream.write(sound)
            except queue.Empty:
                continue

    def notify(self):
        self.sound_queue.put(generate_sound_wave())

    def shutdown(self):
        self.active = False
        self.worker.join()
        self.stream.stop_stream()
        self.stream.close()
        self.audio.terminate()

def get_current_time():
    return datetime.datetime.now().strftime('%H:%M')

def get_current_date():
    return datetime.datetime.now().strftime('%Y-%m-%d')

def load_log_data(file_path):
    try:
        with open(file_path, 'r') as file:
            return yaml.safe_load(file) or {}
    except FileNotFoundError:
        return {}

def save_log_data(file_path, data):
    with open(file_path, 'w') as file:
        yaml.dump(data, file, sort_keys=False, default_flow_style=False)

def create_task_record(description):
    return {
        'start': get_current_time(),
        'description': description[:200],
        'notes': [],
        'end': None
    }

def add_notes_to_task(task_record):
    while True:
        note = input("Add note (or 'done' to finish): ").strip()
        if note.lower() == 'done':
            break
        task_record['notes'].append({
            'time': get_current_time(),
            'content': note[:200]
        })

def calculate_duration(start, end):
    try:
        start_time = datetime.datetime.strptime(start, '%H:%M')
        end_time = datetime.datetime.strptime(end, '%H:%M')
        duration = end_time - start_time
        total_seconds = duration.total_seconds()
        hours = int(total_seconds // 3600)
        minutes = int((total_seconds % 3600) // 60)
        return f"{hours:02d}:{minutes:02d}"
    except:
        return "00:00"

def complete_task_record(task_record):
    task_record['end'] = get_current_time()
    duration = calculate_duration(task_record['start'], task_record['end'])
    print(f"Task duration: {duration}")
    task_record['duration'] = duration

def get_task_description(task):
    return task.get('description', task.get('task', 'No description'))

def get_task_notes(task):
    return task.get('notes', task.get('changes', []))

def show_full_log(data):
    for date, tasks in data.items():
        print(f"\n{date}")
        for task in tasks:
            print(f"  {get_task_description(task)}")
            print(f"  {task.get('start', '')} - {task.get('end', '')} ({task.get('duration', '00:00')})")
            for note in get_task_notes(task):
                print(f"    {note.get('time', '')}: {note.get('content', note.get('note', ''))}")

def show_daily_log(data, date):
    if date not in data:
        print("No tasks for this date.")
        return
    
    print(f"\n{date}")
    for task in data[date]:
        print(f"  {get_task_description(task)}")
        print(f"  {task.get('start', '')} - {task.get('end', '')} ({task.get('duration', '00:00')})")
        for note in get_task_notes(task):
            print(f"    {note.get('time', '')}: {note.get('content', note.get('note', ''))}")

def show_descriptions_only(data):
    for date, tasks in data.items():
        print(f"\n{date}")
        for task in tasks:
            print(f"  {get_task_description(task)}")

def handle_new_task(sound_notifier):
    log_data = load_log_data(LOG_FILE)
    current_date = get_current_date()

    description = input("Enter task description: ").strip()
    task_record = create_task_record(description)

    print("Task started. Add notes as needed...")
    add_notes_to_task(task_record)

    complete_task_record(task_record)
    log_data.setdefault(current_date, []).append(task_record)
    save_log_data(LOG_FILE, log_data)
    sound_notifier.notify()

def display_main_menu():
    print("\nTask Tracker:")
    print("1. Start new task")
    print("2. View complete log")
    print("3. View today's log")
    print("4. View descriptions only")
    print("5. Exit")
    return input("Select: ").strip()

def handle_menu_choice(choice, sound_notifier):
    if choice == '1':
        handle_new_task(sound_notifier)
    elif choice == '2':
        show_full_log(load_log_data(LOG_FILE))
    elif choice == '3':
        default_date = get_current_date()
        date = input(f"Date [{default_date}]: ").strip() or default_date
        show_daily_log(load_log_data(LOG_FILE), date)
    elif choice == '4':
        show_descriptions_only(load_log_data(LOG_FILE))
    elif choice == '5':
        return False
    else:
        print("Invalid selection.")
    return True

def initialize_system():
    notifier = SoundNotifier()
    notifier.notify()
    return notifier

def run_application():
    sound_notifier = initialize_system()
    try:
        while True:
            choice = display_main_menu()
            if not handle_menu_choice(choice, sound_notifier):
                break
    except KeyboardInterrupt:
        print("\nApplication interrupted.")
    finally:
        sound_notifier.shutdown()

LOG_FILE = Path(r'c:\atari-monk\code\apps-data-store\stuff_done_log.yaml')

def main():
    try:
        run_application()
    except ImportError as e:
        print(f"Missing required library: {e.name}")
        sys.exit(1)

if __name__ == "__main__":
    main()