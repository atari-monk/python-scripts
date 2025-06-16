#!/usr/bin/env python3
import argparse
from dataclasses import dataclass, field, asdict
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Optional, Dict, Any
import tomli_w
import tomllib

MAX_NOTE_LENGTH = 300
TRACKING_FILE = r"C:\atari-monk\code\apps-data-store\tracking.toml"

@dataclass
class TrackingNote:
    time: str
    text: str

@dataclass
class TrackingBreak:
    start: str
    end: Optional[str] = None
    duration_minutes: Optional[float] = None

@dataclass
class TrackingSession:
    id: str
    start: str
    stop: Optional[str] = None
    duration_minutes: Optional[float] = None
    breaks: List[TrackingBreak] = field(default_factory=list)
    notes: List[TrackingNote] = field(default_factory=list)
    paused: bool = False

@dataclass
class TrackingData:
    entries: List[TrackingSession] = field(default_factory=list)
    active_session: Optional[str] = None

class TrackingStorage:
    def __init__(self, file_path: str = TRACKING_FILE):
        self.file_path = Path(file_path)
    
    def load(self) -> TrackingData:
        if not self.file_path.exists():
            return TrackingData()
        
        with open(self.file_path, "rb") as f:
            data = tomllib.load(f)
            return self._deserialize(data)
    
    def save(self, data: TrackingData) -> None:
        with open(self.file_path, "wb") as f:
            tomli_w.dump(self._prepare_for_toml(data), f)
    
    def _prepare_for_toml(self, data: TrackingData) -> Dict[str, Any]:
        result = {
            "active_session": data.active_session if data.active_session else "",
            "entries": []
        }
        
        for entry in data.entries:
            entry_dict = {
                "id": entry.id,
                "start": entry.start,
                "stop": entry.stop if entry.stop else "",
                "duration_minutes": entry.duration_minutes if entry.duration_minutes else 0.0,
                "paused": entry.paused,
                "breaks": [
                    {
                        "start": b.start,
                        "end": b.end if b.end else "",
                        "duration_minutes": b.duration_minutes if b.duration_minutes else 0.0
                    }
                    for b in entry.breaks
                ],
                "notes": [asdict(note) for note in entry.notes]
            }
            result["entries"].append(entry_dict)
        
        return result
    
    def _deserialize(self, raw: dict) -> TrackingData:
        return TrackingData(
            active_session=raw.get("active_session") or None,
            entries=[
                TrackingSession(
                    id=entry["id"],
                    start=entry["start"],
                    stop=entry.get("stop") or None,
                    duration_minutes=entry.get("duration_minutes") or None,
                    paused=entry.get("paused", False),
                    breaks=[
                        TrackingBreak(
                            start=b["start"],
                            end=b.get("end") or None,
                            duration_minutes=b.get("duration_minutes") or None
                        )
                        for b in entry.get("breaks", [])
                    ],
                    notes=[TrackingNote(**note) for note in entry["notes"]]
                )
                for entry in raw.get("entries", [])
            ]
        )

class TrackingManager:
    def __init__(self, storage: TrackingStorage):
        self.storage = storage
        self.data = storage.load()
    
    def validate_note(self, text: Optional[str]) -> Optional[str]:
        if text is not None:
            if not text.strip():
                raise ValueError("Note cannot be empty")
            if len(text) > MAX_NOTE_LENGTH:
                raise ValueError(f"Note exceeds maximum length of {MAX_NOTE_LENGTH} chars")
        return text

    def get_current_session(self) -> Optional[TrackingSession]:
        # Always load fresh data first
        self.data = self.storage.load()
        if not self.data.active_session:
            return None
        session = next((e for e in self.data.entries if e.id == self.data.active_session), None)
        return session
    
    def start_tracking(self, note: Optional[str] = None) -> None:
        if self.data.active_session:
            print("Error: Session already active")
            return
        
        timestamp = datetime.now().isoformat()
        session_id = datetime.now().strftime("%Y%m%d%H%M%S")
        
        new_session = TrackingSession(id=session_id, start=timestamp)
        if note:
            new_session.notes.append(TrackingNote(time=timestamp, text=note))
        
        self.data.entries.append(new_session)
        self.data.active_session = session_id
        self.storage.save(self.data)
        
        print(f"Started tracking at {timestamp}" + (f" | Note: {note}" if note else ""))
    
    def pause_tracking(self, note: Optional[str] = None) -> None:
        if not (session := self.get_current_session()):
            print("Error: No active session to pause")
            return
        
        if session.paused:
            print("Error: Session already paused")
            return
        
        timestamp = datetime.now().isoformat()
        session.breaks.append(TrackingBreak(start=timestamp))
        session.paused = True
        if note:
            session.notes.append(TrackingNote(time=timestamp, text=f"Paused: {note}"))
        self.storage.save(self.data)
        
        print(f"Paused tracking at {timestamp}" + (f" | Note: {note}" if note else ""))
    
    def resume_tracking(self, note: Optional[str] = None) -> None:
        if not (session := self.get_current_session()):
            print("Error: No active session to resume")
            return
        
        if not session.paused:
            print("Error: Session not paused")
            return
        
        if not session.breaks or session.breaks[-1].end is not None:
            print("Error: No active break to resume from")
            return
        
        timestamp = datetime.now().isoformat()
        current_break = session.breaks[-1]
        current_break.end = timestamp
        duration = (datetime.fromisoformat(timestamp) - 
                  datetime.fromisoformat(current_break.start)).total_seconds() / 60
        current_break.duration_minutes = round(duration, 2)
        session.paused = False
        if note:
            session.notes.append(TrackingNote(time=timestamp, text=f"Resumed: {note}"))
        self.storage.save(self.data)
        
        duration_str = str(timedelta(minutes=duration)).split(".")[0]
        print(f"Resumed tracking at {timestamp} | Break duration: {duration_str}" + 
              (f" | Note: {note}" if note else ""))
    
    def stop_tracking(self, note: Optional[str] = None) -> None:
        if not (session := self.get_current_session()):
            print("Error: No active session")
            return
        
        if session.paused:
            print("Error: Cannot stop while paused. Resume first.")
            return
        
        timestamp = datetime.now().isoformat()
        
        # Calculate active duration (excluding breaks)
        total_break_time = sum(b.duration_minutes or 0 for b in session.breaks)
        total_duration = (datetime.fromisoformat(timestamp) - 
                       datetime.fromisoformat(session.start)).total_seconds() / 60
        active_duration = total_duration - total_break_time
        
        session.stop = timestamp
        session.duration_minutes = round(active_duration, 2)
        if note:
            session.notes.append(TrackingNote(time=timestamp, text=note))
        self.data.active_session = None
        self.storage.save(self.data)
        
        duration_str = str(timedelta(minutes=active_duration)).split(".")[0]
        print(f"Stopped tracking at {timestamp} | Active duration: {duration_str}" + 
              (f" | Note: {note}" if note else ""))
    
    def add_note(self, note: str) -> None:
        if not note.strip():
            print("Error: Cannot add an empty note")
            return
        if not (session := self.get_current_session()):
            print("Error: No active session")
            return
        
        timestamp = datetime.now().isoformat()
        session.notes.append(TrackingNote(time=timestamp, text=note))
        self.storage.save(self.data)
        print(f"Note added at {timestamp}: {note}")
    
    def show_status(self) -> None:
        if not (session := self.get_current_session()):
            print("No active session")
            return
        
        now = datetime.now()
        start_time = datetime.fromisoformat(session.start)
        
        if session.paused:
            status = "PAUSED"
            last_break = session.breaks[-1] if session.breaks else None
            if last_break and last_break.end is None:
                break_duration = (now - datetime.fromisoformat(last_break.start)).total_seconds() / 60
                duration_str = str(timedelta(minutes=break_duration)).split(".")[0]
                print(f"Break duration: {duration_str}")
        else:
            status = "ACTIVE"
            total_break_time = sum(b.duration_minutes or 0 for b in session.breaks)
            total_duration = (now - start_time).total_seconds() / 60
            active_duration = total_duration - total_break_time
            duration_str = str(timedelta(minutes=active_duration)).split(".")[0]
            print(f"Active duration: {duration_str}")
        
        print(f"Status: {status}")
        print(f"Session started at {session.start}")
        print(f"Breaks taken: {len(session.breaks)}")
        if session.notes:
            print("Recent notes:")
            for note in session.notes[-5:]:
                print(f"  {note.time}: {note.text}")
    
    def show_history(self, days: int = 7) -> None:
        cutoff = datetime.now() - timedelta(days=days)
        print(f"Last {days} days history:")
        print("=" * 50)
        
        for entry in reversed(self.data.entries):
            if datetime.fromisoformat(entry.start) < cutoff:
                continue
            
            duration = f"{entry.duration_minutes:.0f}min" if entry.duration_minutes else "Active"
            print(f"Session {entry.id}:")
            print(f"  Start:  {entry.start}")
            print(f"  Stop:   {entry.stop or 'Still active'}")
            print(f"  Duration: {duration}")
            print(f"  Breaks: {len(entry.breaks)}")
            if entry.notes:
                print("  Notes:")
                for note in entry.notes:
                    print(f"    {note.time}: {note.text}")
            print("-" * 50)
    
    def show_summary(self, today_only: bool = False) -> None:
        cutoff = (datetime.now().replace(hour=0, minute=0, second=0) 
                if today_only else datetime.now() - timedelta(days=30))
        
        sessions = [e for e in self.data.entries if datetime.fromisoformat(e.start) >= cutoff]
        total_time = sum(e.duration_minutes or 0 for e in sessions)
        total_breaks = sum(len(e.breaks) for e in sessions)
        
        print(f"Summary ({'today' if today_only else 'last 30 days'}):")
        print("=" * 50)
        print(f"Sessions:  {len(sessions)}")
        print(f"Total time: {total_time/60:.1f} hours")
        print(f"Total breaks: {total_breaks}")
        print(f"Avg session: {total_time/len(sessions):.1f} min" if sessions else "No sessions")
        print(f"Total notes: {sum(len(e.notes) for e in sessions)}")
        print("=" * 50)

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