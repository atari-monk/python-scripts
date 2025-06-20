import argparse
import pyperclip
from dataclasses import dataclass, asdict, field
from pathlib import Path
import json
from typing import Dict, Optional, List
import os

@dataclass
class BlogConfig:
    targets: Dict[str, str] = field(default_factory=lambda: {})
    last_used_target: Optional[str] = None

def get_config_path() -> Path:
    return Path(r"C:\atari-monk\code\apps-data-store\blog_config.json")

def load_config() -> BlogConfig:
    config_path = get_config_path()
    try:
        if config_path.exists() and config_path.stat().st_size > 0:
            with open(config_path, "r") as f:
                data = json.load(f)
                if "targets" in data:
                    return BlogConfig(
                        targets=data["targets"],
                        last_used_target=data.get("last_used_target")
                    )
                elif "repos" in data:
                    return BlogConfig(targets=data["repos"])
                else:
                    return BlogConfig(targets={"blog": data.get("repo_path", "")})
    except (json.JSONDecodeError, AttributeError):
        print("Warning: Config file corrupted, creating new one")
    return BlogConfig()

def save_config(config: BlogConfig) -> None:
    with open(get_config_path(), "w") as f:
        json.dump(asdict(config), f, indent=2)

def get_target_categories(target_path: Path) -> List[str]:
    categories = []
    for root, dirs, files in os.walk(target_path):
        rel_path = os.path.relpath(root, target_path)
        if rel_path != ".":
            categories.append(rel_path.replace("\\", "/"))
    return sorted(set(categories))

def print_categories(categories: List[str], filter_term: str = None) -> None:
    if not categories:
        print("No categories found")
        return
    
    if filter_term:
        categories = [c for c in categories if filter_term.lower() in c.lower()]
        if not categories:
            print(f"No categories matching '{filter_term}'")
            return
    
    # Group by top-level categories
    tree = {}
    for category in categories:
        parts = category.split("/")
        node = tree
        for part in parts[:-1]:
            node = node.setdefault(part, {})
        node[parts[-1]] = None
    
    def print_tree(node, prefix=""):
        keys = sorted(node.keys())
        for i, key in enumerate(keys):
            if i == len(keys) - 1:
                new_prefix = prefix + "    "
                print(prefix + "└── " + key)
            else:
                new_prefix = prefix + "│   "
                print(prefix + "├── " + key)
            if node[key] is not None:
                print_tree(node[key], new_prefix)
    
    print_tree(tree)

def select_target(config: BlogConfig, target_name: Optional[str] = None) -> Path:
    if target_name and target_name in config.targets:
        path = config.targets[target_name]
        if not path:
            path = input(f"Enter path for target '{target_name}': ").strip()
            config.targets[target_name] = path
            save_config(config)
        config.last_used_target = target_name
        save_config(config)
        return Path(path).resolve()
    
    print("\nAvailable targets:")
    for i, (name, path) in enumerate(config.targets.items(), 1):
        active = " *" if name == config.last_used_target else ""
        print(f"{i}. {name}: {path if path else 'Not configured'}{active}")
    
    while True:
        choice = input("\nSelect target (1-{}), 'a' to add new: ".format(
            len(config.targets))).strip().lower()
        
        if choice == "a":
            new_name = input("Enter new target name: ").strip()
            new_path = input(f"Enter path for {new_name}: ").strip()
            config.targets[new_name] = new_path
            config.last_used_target = new_name
            save_config(config)
            return Path(new_path).resolve()
        
        try:
            choice_num = int(choice)
            if 1 <= choice_num <= len(config.targets):
                selected_name = list(config.targets.keys())[choice_num-1]
                path = config.targets[selected_name]
                if not path:
                    path = input(f"Enter path for {selected_name}: ").strip()
                    config.targets[selected_name] = path
                    save_config(config)
                config.last_used_target = selected_name
                save_config(config)
                return Path(path).resolve()
        except ValueError:
            pass
        print("Invalid selection, please try again")

def create_folder_if_not_exists(path: Path) -> None:
    if not path.exists():
        path.mkdir(parents=True)

def main():
    parser = argparse.ArgumentParser(description="Content manager")
    parser.add_argument("-t", "--target", help="Specify target name")
    parser.add_argument("-c", "--category", help="Specify category path (e.g. 'tech/python')")
    parser.add_argument("-f", "--file", help="Specify filename (without extension)")
    parser.add_argument("-l", "--list", action="store_true", help="List available targets")
    parser.add_argument("-lc", "--list-categories", action="store_true", 
                       help="List categories in target")
    parser.add_argument("-s", "--search", metavar="TERM", 
                       help="Search/filter categories by name")
    parser.add_argument("-a", "--add", metavar="NAME", help="Add a new target")
    args = parser.parse_args()

    config = load_config()

    if args.add:
        path = input(f"Enter path for target '{args.add}': ").strip()
        config.targets[args.add] = path
        config.last_used_target = args.add
        save_config(config)
        print(f"Added target '{args.add}' with path '{path}'")
        return

    if args.list:
        print("Configured targets:")
        for name, path in config.targets.items():
            active = " *" if name == config.last_used_target else ""
            print(f"{name}: {path if path else 'Not configured'}{active}")
        return

    # Handle category listing/search
    if args.list_categories or args.search:
        target_path = select_target(config, args.target)
        categories = get_target_categories(target_path)
        
        if args.search:
            print(f"Categories matching '{args.search}':")
            print_categories(categories, args.search)
        else:
            print("Available categories:")
            print_categories(categories)
        return

    # Normal file saving operation
    target_path = select_target(config, args.target)
    
    category = args.category if args.category else input(
        "Enter category path (e.g. 'tech/python' or leave empty): ").strip()
    
    filename = args.file if args.file else input(
        "Enter filename (without extension): ").strip()
    
    full_path = target_path / category if category else target_path
    create_folder_if_not_exists(full_path)
    
    input("Copy content to clipboard and press Enter...")
    content = pyperclip.paste()
    
    file_path = full_path / f"{filename}.md"
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
    
    print(f"Saved to: {file_path}")

if __name__ == "__main__":
    main()