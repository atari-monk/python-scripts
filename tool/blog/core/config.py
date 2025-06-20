from dataclasses import dataclass, field
from typing import Dict


@dataclass
class Config:
    targets: Dict[str, str] = field(default_factory=lambda: {})