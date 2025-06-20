from plumbum import cli
from tool.blog.core.config_crud import ConfigCRUD
import os

from tool.blog.core.helper import select_target_interactive

class ListCategory(cli.Application):
    
    search_term = cli.SwitchAttr(
        ['-s', '--search'],
        help="Filter categories by search term"
    )
    
    def main(self, target_name: str = None):
        config = ConfigCRUD.load()
        
        try:
            target_path = select_target_interactive(config, target_name)
        except ValueError:
            return 1
        
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