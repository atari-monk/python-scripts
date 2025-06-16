from typing import List, Optional
from dataclasses import dataclass, field

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
