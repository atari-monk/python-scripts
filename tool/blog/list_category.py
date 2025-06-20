from plumbum import cli
from tool.blog.core.config_crud import ConfigCRUD
import os

from tool.blog.core.cli import select_target_interactive
from tool.blog.core.file_sys import build_category_tree, print_category_tree

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
        
        if not categories:
            print("No categories found")
            return
        
        if self.search_term:
            categories = [c for c in categories if self.search_term.lower() in c.lower()]
            if not categories:
                print(f"No categories matching '{self.search_term}'")
                return
        
        tree = build_category_tree(categories)
        print("Available categories:")
        print_category_tree(tree)