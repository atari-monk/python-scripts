from typing import Optional
from datetime import datetime, timedelta
from tool.tracker.config import MAX_NOTE_LENGTH
from tool.tracker.model import TrackingBreak, TrackingNote, TrackingSession
from tool.tracker.storage import TrackingStorage

class TrackingService:
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