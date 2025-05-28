from pathlib import Path

class SimpleFolderIndexer:
    def __init__(self, root_path: str):
        self.root = Path(root_path).resolve()
        
    def generate(self):
        index_lines = ["# Documentation Index\n"]
        
        for path in sorted(self.root.glob("**/*.md")):
            if path.name == "index.md":
                continue
                
            rel_path = path.relative_to(self.root)
            name = path.stem.replace("_", " ").title()
            indent = "  " * (len(rel_path.parts) - 1)
            index_lines.append(f"{indent}- [{name}]({rel_path})")
            
        (self.root / "index.md").write_text("\n".join(index_lines))