from plumbum import cli
from tool.blog.core.config_crud import ConfigCRUD
from pathlib import Path

class EditTarget(cli.Application):
    """Update the path of an existing target"""
    
    def main(self, target_name: str = None, new_path: str = None):
        config = ConfigCRUD.load()
        
        if not config.targets:
            print("No targets configured. Use 'add-target' first.")
            return 1
            
        # If no target specified, show interactive selection
        if not target_name:
            print("Available targets:")
            for i, (name, path) in enumerate(config.targets.items(), 1):
                print(f"{i}. {name}: {path}")
            
            while True:
                choice = input("\nSelect target to edit (1-{}): ".format(
                    len(config.targets))).strip()
                
                try:
                    choice_num = int(choice)
                    if 1 <= choice_num <= len(config.targets):
                        target_name = list(config.targets.keys())[choice_num-1]
                        break
                except ValueError:
                    pass
                print("Invalid selection")
        
        # Verify target exists
        if target_name not in config.targets:
            print(f"Target '{target_name}' doesn't exist")
            return 1
            
        # Get new path if not provided
        current_path = config.targets[target_name]
        if not new_path:
            print(f"Current path for '{target_name}': {current_path}")
            new_path = input("Enter new path (leave empty to keep current): ").strip()
            
        # Update if new path was provided
        if new_path:
            config.targets[target_name] = new_path
            ConfigCRUD.save(config)
            print(f"Updated target '{target_name}'")
            print(f"Old path: {current_path}")
            print(f"New path: {new_path}")
        else:
            print("Path unchanged")
        
        return 0