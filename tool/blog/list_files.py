from plumbum import cli
from tool.blog.core.config_crud import ConfigCRUD
from pathlib import Path
import os

class ListFiles(cli.Application):
    """List all files in a target repository, optionally filtered by category"""
    
    search_term = cli.SwitchAttr(
        ['-s', '--search'],
        help="Filter files by search term"
    )
    
    category = cli.SwitchAttr(
        ['-c', '--category'],
        help="Specific category to list files from"
    )
    
    def _select_target(self, config, target_name: str = None) -> Path:
        """Shared target selection logic"""
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
    
    def main(self, target_name: str = None):
        config = ConfigCRUD.load()
        
        try:
            target_path = self._select_target(config, target_name)
        except ValueError:
            return 1
        
        # Collect files
        files = []
        if self.category:
            search_path = target_path / self.category
            if not search_path.exists():
                print(f"Category '{self.category}' not found")
                return 1
                
            for item in search_path.iterdir():
                if item.is_file() and item.suffix == '.md':
                    files.append((self.category, item.name))
        else:
            for root, _, filenames in os.walk(target_path):
                rel_path = os.path.relpath(root, target_path)
                if rel_path == '.':
                    category = ''
                else:
                    category = rel_path.replace("\\", "/")
                
                for filename in filenames:
                    if filename.endswith('.md'):
                        files.append((category, filename))
        
        # Filter files
        if self.search_term:
            files = [
                (cat, f) for cat, f in files 
                if self.search_term.lower() in f.lower()
            ]
        
        # Sort and display
        files.sort(key=lambda x: (x[0], x[1]))
        
        if not files:
            print("No markdown files found")
            return
        
        print("\nFound files:")
        current_category = None
        for category, filename in files:
            if category != current_category:
                if category:
                    print(f"\n[{category}]")
                else:
                    print("\n[Uncategorized]")
                current_category = category
            print(f"  {filename}")
        
        print(f"\nTotal files: {len(files)}")
        return 0