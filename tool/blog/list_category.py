from plumbum import cli
from tool.blog.core.config_crud import ConfigCRUD
from pathlib import Path
import os

class ListCategory(cli.Application):
    """List all categories in the target repository"""
    
    search_term = cli.SwitchAttr(
        ['-s', '--search'],
        help="Filter categories by search term"
    )
    
    def main(self, target_name: str = None):
        config = ConfigCRUD.load()
        
        # Select target
        if target_name and target_name in config.targets:
            target_path = Path(config.targets[target_name])
            if not target_path:
                print(f"Error: Path not configured for target '{target_name}'")
                return 1
        else:
            # Interactive target selection
            if not config.targets:
                print("No targets configured. Use 'add-target' first.")
                return 1
                
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
                        target_path = Path(config.targets[selected_name])
                        if not target_path:
                            print(f"Error: Path not configured for target '{selected_name}'")
                            return 1
                        break
                except ValueError:
                    pass
                print("Invalid selection, please try again")
        
        # Get categories
        categories = []
        for root, dirs, files in os.walk(target_path):
            rel_path = os.path.relpath(root, target_path)
            if rel_path != ".":
                categories.append(rel_path.replace("\\", "/"))
        categories = sorted(set(categories))
        
        # Print categories
        if not categories:
            print("No categories found")
            return
        
        if self.search_term:
            categories = [c for c in categories if self.search_term.lower() in c.lower()]
            if not categories:
                print(f"No categories matching '{self.search_term}'")
                return
        
        # Group by top-level categories
        tree = {}
        for category in categories:
            parts = category.split("/")
            node = tree
            for part in parts[:-1]:
                if part not in node:
                    node[part] = {}
                elif node[part] is None:  # Convert leaf node to branch if needed
                    node[part] = {}
                node = node[part]
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
        
        print("Available categories:")
        print_tree(tree)