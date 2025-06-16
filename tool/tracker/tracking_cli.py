#!/usr/bin/env python3
import argparse
from tool.tracker.tracking_manager import TrackingManager
from tool.tracker.tracking_storage import TrackingStorage

def main():
    parser = argparse.ArgumentParser(description="Time tracking utility")
    subparsers = parser.add_subparsers(dest="command", required=True)
    
    # Start command
    start_parser = subparsers.add_parser("start")
    start_parser.add_argument("-n", "--note", help="Optional note text (max 300 chars)")
    
    # Pause command
    pause_parser = subparsers.add_parser("pause")
    pause_parser.add_argument("-n", "--note", help="Optional note text (max 300 chars)")
    
    # Resume command
    resume_parser = subparsers.add_parser("resume")
    resume_parser.add_argument("-n", "--note", help="Optional note text (max 300 chars)")
    
    # Stop command
    stop_parser = subparsers.add_parser("stop")
    stop_parser.add_argument("-n", "--note", help="Optional note text (max 300 chars)")
    
    # Note command
    note_parser = subparsers.add_parser("note")
    note_parser.add_argument("note", help="Note text (max 300 chars)")
    
    # Status command
    subparsers.add_parser("status")
    
    # History command
    history_parser = subparsers.add_parser("history")
    history_parser.add_argument("--days", type=int, default=7, help="Days to show")
    
    # Summary command
    summary_parser = subparsers.add_parser("summary")
    summary_parser.add_argument("--today", action="store_true", help="Today only")
    
    args = parser.parse_args()
    tracker = TrackingManager(TrackingStorage())
    
    try:
        if args.command == "start":
            tracker.start_tracking(tracker.validate_note(args.note))
        elif args.command == "pause":
            tracker.pause_tracking(tracker.validate_note(args.note))
        elif args.command == "resume":
            tracker.resume_tracking(tracker.validate_note(args.note))
        elif args.command == "stop":
            tracker.stop_tracking(tracker.validate_note(args.note))
        elif args.command == "note":
            tracker.add_note(tracker.validate_note(args.note))
        elif args.command == "status":
            tracker.show_status()
        elif args.command == "history":
            tracker.show_history(args.days)
        elif args.command == "summary":
            tracker.show_summary(args.today)
    except ValueError as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()