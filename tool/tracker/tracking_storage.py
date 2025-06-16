from typing import Any, Dict
from pathlib import Path
from dataclasses import asdict
import tomli_w
import tomllib
from tool.tracker.tracking_cli import TRACKING_FILE, TrackingBreak, TrackingData, TrackingNote, TrackingSession

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