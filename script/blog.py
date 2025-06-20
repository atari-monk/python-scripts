import argparse
import pyperclip
from dataclasses import dataclass, asdict, field
from pathlib import Path
import json
from typing import Dict, Optional

@dataclass
class BlogConfig:
    repos: Dict[str, str] = field(default_factory=lambda: {
        "blog": "",
        "dev-blog": ""
    })

def get_config_path() -> Path:
    return Path(r"C:\atari-monk\code\apps-data-store\blog_config.json")

def load_config() -> BlogConfig:
    config_path = get_config_path()
    try:
        if config_path.exists() and config_path.stat().st_size > 0:
            with open(config_path, "r") as f:
                data = json.load(f)
                return BlogConfig(repos=data.get("repos", {
                    "blog": data.get("repo_path", ""),
                    "dev-blog": ""
                }))
    except (json.JSONDecodeError, AttributeError):
        print("Warning: Config file corrupted, creating new one")
    return BlogConfig()

def save_config(config: BlogConfig) -> None:
    with open(get_config_path(), "w") as f:
        json.dump(asdict(config), f, indent=2)

def select_repo(config: BlogConfig, repo_name: Optional[str] = None) -> Path:
    if repo_name and repo_name in config.repos:
        path = config.repos[repo_name]
        if not path:
            path = input(f"Enter path for {repo_name}: ").strip()
            config.repos[repo_name] = path
            save_config(config)
        return Path(path).resolve()
    
    print("Available repositories:")
    for i, (name, path) in enumerate(config.repos.items(), 1):
        print(f"{i}. {name}: {path if path else 'Not configured'}")
    
    while True:
        choice = input("Select repository (1-2) or 'a' to add new: ").strip().lower()
        if choice == "a":
            new_name = input("Enter new repository name: ").strip()
            new_path = input(f"Enter path for {new_name}: ").strip()
            config.repos[new_name] = new_path
            save_config(config)
            return Path(new_path).resolve()
        
        try:
            if choice.isdigit() and 1 <= int(choice) <= len(config.repos):
                selected = list(config.repos.keys())[int(choice)-1]
                path = config.repos[selected]
                if not path:
                    path = input(f"Enter path for {selected}: ").strip()
                    config.repos[selected] = path
                    save_config(config)
                return Path(path).resolve()
        except (ValueError, IndexError):
            pass
        print("Invalid selection, please try again")

def create_folder_if_not_exists(path: Path) -> None:
    if not path.exists():
        path.mkdir(parents=True)

def main():
    parser = argparse.ArgumentParser(description="Blog content manager")
    parser.add_argument("-r", "--repo", help="Specify repository name (e.g., 'blog' or 'dev-blog')")
    parser.add_argument("-c", "--category", help="Specify category path (e.g., 'tech/python')")
    parser.add_argument("-f", "--file", help="Specify filename (without .md extension)")
    parser.add_argument("--list", action="store_true", help="List available repositories")
    args = parser.parse_args()

    config = load_config()

    if args.list:
        print("Configured repositories:")
        for name, path in config.repos.items():
            print(f"{name}: {path if path else 'Not configured'}")
        return

    repo_path = select_repo(config, args.repo)
    
    category = args.category if args.category else input("Enter category path (e.g. 'tech/python'): ").strip()
    filename = args.file if args.file else input("Enter filename (without .md): ").strip()
    
    category_path = repo_path / category
    create_folder_if_not_exists(category_path)
    
    input("Copy content to clipboard and press Enter...")
    content = pyperclip.paste()
    
    file_path = category_path / f"{filename}.md"
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
    
    print(f"Saved to: {file_path}")

if __name__ == "__main__":
    main()