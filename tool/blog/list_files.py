from plumbum import cli
from tool.blog.core.config_crud import ConfigCRUD
import os

from tool.blog.core.cli import select_target_interactive

class ListFiles(cli.Application):
    
    search_term = cli.SwitchAttr(
        ['-s', '--search'],
        help="Filter files by search term"
    )
    
    category = cli.SwitchAttr(
        ['-c', '--category'],
        help="Specific category to list files from"
    )
    
    def main(self, target_name: str = None):
        config = ConfigCRUD.load()
        
        try:
            # Changed: Using the new core method instead of local _select_target
            target_path = select_target_interactive(config, target_name)
        except ValueError:
            return 1
        
        # Rest of the file remains the same...
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
        
        if self.search_term:
            files = [
                (cat, f) for cat, f in files 
                if self.search_term.lower() in f.lower()
            ]
        
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