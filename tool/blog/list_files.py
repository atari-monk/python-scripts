from plumbum import cli
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
    
    def main(self, target_name: str = None):
        config = ConfigCRUD.load()
        
        try:
            target_path = select_target_interactive(config, target_name)
        except ValueError:
            return 1
        
        files = list_markdown_files(target_path, self.category)
        
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