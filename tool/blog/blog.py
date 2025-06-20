from dataclasses import dataclass, field
from typing import Dict, Optional


@dataclass
class Blog:
    targets: Dict[str, str] = field(default_factory=lambda: {})
    last_used_target: Optional[str] = None