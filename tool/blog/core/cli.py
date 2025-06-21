from pathlib import Path
from typing import Optional
from tool.blog.core.config import Config


def select_target_interactive(config: Config, target_name: Optional[str] = None) -> Path:
        if target_name and target_name in config.targets:
            path = config.targets[target_name]
            if not path:
                print(f"Error: Path not configured for target '{target_name}'")
                raise ValueError("Invalid target path")
            return Path(path).resolve()
        
        print("\nAvailable targets:")
        for i, (name, path) in enumerate(config.targets.items(), 1):
            print(f"{i}. {name}: {path if path else 'Not configured'}")

        while True:
            choice = input("\nSelect target (1-{}): ".format(
                len(config.targets))).strip()
            
            try:
                choice_num = int(choice)
                if 1 <= choice_num <= len(config.targets):
                    selected_name = list(config.targets.keys())[choice_num-1]
                    path = config.targets[selected_name]
                    if not path:
                        print(f"Error: Path not configured for target '{selected_name}'")
                        raise ValueError("Invalid target path")
                    return Path(path).resolve()
            except ValueError:
                pass
            print("Invalid selection, please try again")

def select_target_name_interactive(config: Config, prompt: str = "Select target") -> str:
    if not config.targets:
        raise ValueError("No targets configured")
        
    print(f"\n{prompt}:")
    for i, (name, path) in enumerate(config.targets.items(), 1):
        print(f"{i}. {name}: {path if path else 'Not configured'}")
    
    while True:
        choice = input("\nEnter target number (1-{}): ".format(
            len(config.targets))).strip()
        
        try:
            choice_num = int(choice)
            if 1 <= choice_num <= len(config.targets):
                return list(config.targets.keys())[choice_num-1]
        except ValueError:
            pass
        print("Invalid selection, please try again")

def prompt_for_target_details(config: Config, existing_target: str = None) -> tuple[str, str]:
    if existing_target:
        target_name = existing_target
    else:
        while True:
            target_name = input("Enter target name: ").strip()
            if target_name:
                if target_name in config.targets:
                    print(f"Target '{target_name}' already exists")
                    continue
                break
            print("Error: Target name cannot be empty")
    
    while True:
        target_path = input(f"Enter path for target '{target_name}': ").strip()
        if target_path:
            break
        print("Error: Path cannot be empty")
    
    return target_name, target_path