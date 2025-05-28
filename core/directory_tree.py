import os
from pathlib import Path
from typing import Set, Dict, List

IGNORE: Dict[str, Set[str]] = {
    "dirs": {".git", "node_modules", "__pycache__", "venv", ".venv"},
    "files": {"package-lock.json"}
}

class DirectoryTree:
    def __init__(self, root: str):
        self.root = Path(root).resolve()
        self.repo_name = self.root.name
        
    def generate(self) -> str:
        tree = self._build_tree(self.root)
        return f"# {self.repo_name} File Tree\n\n```\n{tree}\n```"
    
    def _build_tree(self, path: Path, prefix: str = "") -> str:
        try:
            items = sorted(path.iterdir())
        except PermissionError:
            return f"{prefix}└── [Permission denied]"
            
        items = [item for item in items if not self._should_ignore(item)]
        lines: List[str] = []
        
        for i, item in enumerate(items):
            is_last = i == len(items) - 1
            lines.append(f"{prefix}{'└──' if is_last else '├──'} {item.name}")
            
            if item.is_dir():
                new_prefix = prefix + ("    " if is_last else "│   ")
                lines.append(self._build_tree(item, new_prefix))
                
        return "\n".join(lines)
    
    def _should_ignore(self, path: Path) -> bool:
        if path.is_dir() and path.name in IGNORE["dirs"]:
            return True
        return path.is_file() and path.name in IGNORE["files"]