import json
import re
from dataclasses import dataclass
from typing import List
from pathlib import Path
from importlib.metadata import entry_points


@dataclass
class ScriptInfo:
    ScriptName: str
    Description: str

    def __post_init__(self):
        if not re.match(r'^[a-z_]{1,30}$', self.ScriptName):
            raise ValueError("ScriptName must be 1-30 lowercase letters with optional underscores")
        if len(self.Description) > 300:
            raise ValueError("Description must be 300 characters or less")

    @classmethod
    def load_from_file(cls, file_path: Path) -> List["ScriptInfo"]:
        try:
            with open(file_path, "r", encoding='utf-8') as f:
                data = json.load(f)
            return [cls(**item) for item in data]
        except (json.JSONDecodeError, FileNotFoundError) as e:
            raise ValueError(f"Error loading script info: {str(e)}")

    @classmethod
    def save_to_file(cls, scripts: List["ScriptInfo"], file_path: Path):
        with open(file_path, "w") as f:
            json.dump([{"ScriptName": s.ScriptName, "Description": s.Description} for s in scripts], f, indent=2)

    @staticmethod
    def format_list(scripts: List["ScriptInfo"]) -> str:
        return "\n".join(f"{script.ScriptName} : {script.Description}" for script in scripts)

    @staticmethod
    def get_console_scripts() -> List[str]:
        return [f"{ep.name} = {ep.value}" for ep in entry_points().get('console_scripts', [])]