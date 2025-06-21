from plumbum import cli
from pathlib import Path
import os
from tool.blog.core.config_crud import ConfigCRUD
from tool.blog.core.cli import select_target_interactive
from tool.blog.core.file_sys import list_markdown_files


class ListFiles(cli.Application):
    
    search_term = cli.SwitchAttr(
        ['-s', '--search'],
        help="Filter files by search term"
    )
    
    category = cli.SwitchAttr(
        ['-c', '--category'],
        help="Specific category to list files from"
    )
    
    verbose = cli.Flag(
        ['-v', '--verbose'],
        help="Enable verbose output for debugging"
    )
    
    def main(self, target_name: str = None):
        config = ConfigCRUD.load()
        
        try:
            target_path = select_target_interactive(config, target_name)
            if self.verbose:
                print(f"DEBUG: Selected target path: {target_path}")
        except ValueError as e:
            if self.verbose:
                print(f"DEBUG: Error selecting target: {e}")
            return 1
        
        files = list_markdown_files(Path(target_path), self.category, self.verbose)
        
        if self.search_term:
            files = [
                (cat, f) for cat, f in files 
                if self.search_term.lower() in f.lower()
            ]
        
        if not files:
            print("No markdown files found")
            if self.verbose:
                print("DEBUG: Potential issues:")
                print(f"- Target path exists: {Path(target_path).exists()}")
                if self.category:
                    category_path = Path(target_path) / self.category
                    print(f"- Category path exists: {category_path.exists()}")
                print(f"- Directory contents: {os.listdir(target_path)}")
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