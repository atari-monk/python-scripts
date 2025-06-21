from pathlib import Path
import subprocess
import sys
from typing import List, Tuple, Optional
import os

def list_markdown_files(target_path: Path, category: Optional[str] = None, verbose: bool = False) -> List[Tuple[str, str]]:
        files = []
        search_path = target_path / category if category else target_path
        
        if verbose:
            print(f"DEBUG: Searching in path: {search_path}")
            
        if not search_path.exists():
            if verbose:
                print(f"DEBUG: Path does not exist: {search_path}")
            return []
            
        if verbose:
            print(f"DEBUG: Path exists. Walking directory...")
            
        for root, _, filenames in os.walk(search_path):
            rel_path = os.path.relpath(root, target_path)
            if rel_path == '.':
                file_category = ''
            else:
                file_category = rel_path.replace("\\", "/")
            
            if verbose:
                print(f"DEBUG: Current directory: {root} (category: '{file_category}')")
                print(f"DEBUG: Files in directory: {filenames}")
            
            for filename in filenames:
                if filename.lower().endswith('.md'):
                    files.append((file_category, filename))
                    if verbose:
                        print(f"DEBUG: Found markdown file: {filename} in category: {file_category}")
        
        return sorted(files, key=lambda x: (x[0], x[1]))

def select_file_interactive(files: List[Tuple[str, str]]) -> Tuple[str, str]:
    print("\nAvailable files:")
    for i, (category, filename) in enumerate(files, 1):
        display_category = f"[{category}] " if category else ""
        print(f"{i}. {display_category}{filename}")
    
    while True:
        choice = input("\nSelect file (1-{}): ".format(len(files))).strip()
        
        try:
            choice_num = int(choice)
            if 1 <= choice_num <= len(files):
                return files[choice_num-1]
        except ValueError:
            pass
        print("Invalid selection, please try again")

def build_category_tree(categories: List[str]) -> dict:
    tree = {}
    for category in categories:
        parts = category.split("/")
        node = tree
        for part in parts[:-1]:
            if part not in node:
                node[part] = {}
            elif node[part] is None:
                node[part] = {}
            node = node[part]
        node[parts[-1]] = None
    return tree

def print_category_tree(tree: dict, prefix: str = "") -> None:
    keys = sorted(tree.keys())
    for i, key in enumerate(keys):
        if i == len(keys) - 1:
            new_prefix = prefix + "    "
            print(prefix + "└── " + key)
        else:
            new_prefix = prefix + "│   "
            print(prefix + "├── " + key)
        if tree[key] is not None:
            print_category_tree(tree[key], new_prefix)

def open_file_with_default_editor(file_path: Path, editor: str = None) -> None:
    try:
        if editor:
            subprocess.run([editor, file_path], check=True)
        elif sys.platform == 'win32':
            os.startfile(file_path)
        elif sys.platform == 'darwin':
            subprocess.run(['open', file_path], check=True)
        else:
            subprocess.run(['xdg-open', file_path], check=True)
    except Exception as e:
        print(f"Failed to open file: {e}")
        raise