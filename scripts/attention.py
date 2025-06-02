from collections import defaultdict
import time
from pathlib import Path

def save_focus_state_to_yaml(log_file_path, message):
    timestamp = time.strftime('%Y-%m-%d %H:%M')
    date, current_time = timestamp.split(' ')
    data = defaultdict(dict)

    if log_file_path.exists():
        with open(log_file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        current_date = None
        for line in lines:
            line = line.strip()
            if not line:
                continue
            if line.endswith(':'):
                current_date = line[:-1].strip()
            elif current_date is not None and ': ' in line:
                time_part, msg_part = line.split(': ', 1)
                data[current_date][time_part.strip()] = msg_part.strip()

    data[date][current_time] = message.lower()

    with open(log_file_path, 'w', encoding='utf-8') as f:
        for d in sorted(data.keys()):
            f.write(f"{d}:\n")
            for t in sorted(data[d].keys()):
                f.write(f"  {t}: {data[d][t]}\n")

def display_focus_logs(log_file_path):
    if not log_file_path.exists():
        print("No records found.")
        return

    with open(log_file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    print("\n📘 Full Focus Log:\n")

    if not lines:
        print("No entries found.")
        return    

    for line in lines:
        print(line.rstrip())

def display_focus_logs_for_date(log_file_path, date=None):
    if not log_file_path.exists():
        print("No records found.")
        return

    if date is None:
        date = time.strftime('%Y-%m-%d')

    with open(log_file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    print(f"\n📅 Focus Log for {date}:\n")

    inside_date_section = False
    found_entries = False
    for line in lines:
        stripped = line.strip()
        if stripped == f"{date}:":
            inside_date_section = True
            found_entries = True
            continue
        if inside_date_section:
            # If we hit another date section, stop
            if stripped.endswith(':') and stripped != f"{date}:":
                break
            print(line.rstrip())

    if not found_entries:
        print("No entries found for this date.")

def prompt_focus_state_and_log(log_file_path):
    print("\n🔔 Focus Check-In Menu")
    print("1: 🚀 In Flow")
    print("2: 😐 Neutral")
    print("3: 😩 Struggling")
    print("4: 🤯 Overwhelmed")
    print("5: 🛑 Need Break")
    print("6: 📊 View Records for Date")
    print("7: 📆 View All")

    choice = input("Select an option (1-7): ").strip()

    focus_states = {
        "1": "🚀 in flow",
        "2": "😐 neutral",
        "3": "😩 struggling",
        "4": "🤯 overwhelmed",
        "5": "🛑 need break"
    }

    if choice == "6":
        default_date = time.strftime('%Y-%m-%d')
        date_input = input(f"date (default {default_date}): ").strip() or default_date
        print(f"\nYou selected date: {date_input}")
        display_focus_logs_for_date(log_file_path, date_input)
        return None

    elif choice == "7":
        display_focus_logs(log_file_path)
        return None

    elif choice in focus_states:
        note = input("Add optional note (or press Enter): ").strip()
        message = focus_states[choice] + (f" - {note.lower()}" if note else "")
        save_focus_state_to_yaml(log_file_path, message)
        print(f"\n✅ Logged: {message}\n")
        return message

    else:
        print("\n⚠️ Invalid choice. Try again.\n")
        return None

def run_focus_checkin_loop(log_file_path):
    print("\n🎯 Continuous Focus Check-In (Press Ctrl+C to quit)")

    try:
        while True:
            prompt_focus_state_and_log(log_file_path)

    except KeyboardInterrupt:
        print("\n⏹️ Check-ins stopped.")

def main():
    run_focus_checkin_loop(Path(r"C:\atari-monk\code\apps-data-store\attention_log.yaml"))

if __name__ == "__main__":
    main()