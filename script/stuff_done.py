from pathlib import Path
import yaml
import datetime
import sys

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
        'description': description[:200],
        'start': get_current_time(),
        'end': None,
        'duration': None,
        'notes': []
    }

def add_notes_to_task(task_record, log_data, current_date, task_index):
    while True:
        note = input("Add note (or 'done' to finish): ").strip()
        if note.lower() == 'done':
            break
        new_note = {
            'time': get_current_time(),
            'content': note[:200]
        }
        task_record['notes'].append(new_note)
        # Save after each note
        log_data[current_date][task_index] = task_record
        save_log_data(LOG_FILE, log_data)

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

def complete_task_record(task_record, log_data, current_date, task_index):
    task_record['end'] = get_current_time()
    duration = calculate_duration(task_record['start'], task_record['end'])
    print(f"Task duration: {duration}")
    task_record['duration'] = duration
    # Save completion
    log_data[current_date][task_index] = task_record
    save_log_data(LOG_FILE, log_data)

def get_task_description(task):
    return task.get('description', 'No description')

def get_task_notes(task):
    return task.get('notes', [])

def show_full_log(data):
    for date, tasks in sorted(data.items(), reverse=True):
        print(f"\n{date}")
        for task in tasks:
            print(f"  {get_task_description(task)}")
            print(f"  {task.get('start', '')} - {task.get('end', '')} ({task.get('duration', '00:00')})")
            for note in get_task_notes(task):
                print(f"    {note.get('time', '')}: {note.get('content', '')}")

def show_daily_log(data, date):
    if date not in data:
        print("No tasks for this date.")
        return
    
    print(f"\n{date}")
    for task in data[date]:
        print(f"  {get_task_description(task)}")
        print(f"  {task.get('start', '')} - {task.get('end', '')} ({task.get('duration', '00:00')})")
        for note in get_task_notes(task):
            print(f"    {note.get('time', '')}: {note.get('content', '')}")

def show_descriptions_only(data):
    for date, tasks in sorted(data.items(), reverse=True):
        print(f"\n{date}")
        for task in tasks:
            print(f"  {get_task_description(task)}")

def handle_new_task():
    log_data = load_log_data(LOG_FILE)
    current_date = get_current_date()

    description = input("Enter task description: ").strip()
    task_record = create_task_record(description)
    
    # Initialize task in log
    if current_date not in log_data:
        log_data[current_date] = []
    task_index = len(log_data[current_date])
    log_data[current_date].append(task_record)
    save_log_data(LOG_FILE, log_data)

    print("Task started. Add notes as needed...")
    add_notes_to_task(task_record, log_data, current_date, task_index)

    complete_task_record(task_record, log_data, current_date, task_index)

def display_main_menu():
    print("\nTask Tracker:")
    print("1. Start new task")
    print("2. View complete log")
    print("3. View specific date log")
    print("4. View descriptions only")
    print("5. Exit")
    return input("Select: ").strip()

def handle_menu_choice(choice):
    if choice == '1':
        handle_new_task()
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

def run_application():
    try:
        while True:
            choice = display_main_menu()
            if not handle_menu_choice(choice):
                break
    except KeyboardInterrupt:
        print("\nApplication interrupted.")

LOG_FILE = Path(r'c:\atari-monk\code\apps-data-store\stuff_done_log.yaml')

def main():
    try:
        run_application()
    except ImportError as e:
        print(f"Missing required library: {e.name}")
        sys.exit(1)

if __name__ == "__main__":
    main()