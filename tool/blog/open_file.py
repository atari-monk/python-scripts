from plumbum import cli
from tool.blog.core.config_crud import ConfigCRUD
import os
import subprocess
import sys

from tool.blog.core.cli import select_target_interactive
from tool.blog.core.file_sys import list_markdown_files, open_file_with_default_editor, select_file_interactive

class OpenFile(cli.Application):
    
    category = cli.SwitchAttr(
        ['-c', '--category'],
        help="Category path (e.g. 'tech/python')"
    )
    
    editor = cli.SwitchAttr(
        ['-e', '--editor'],
        help="Specify editor command (default: system default)"
    )
    
    def main(self, target_name: str = None, filename: str = None):
        config = ConfigCRUD.load()
        
        try:
            target_path = select_target_interactive(config, target_name)
        except ValueError:
            return 1
        
        files = list_markdown_files(target_path, self.category)
        if filename and not self.category:
            matching_files = [
                (cat, f) for cat, f in files 
                if f.lower() == filename.lower() or 
                   f.lower() == f"{filename.lower()}.md"
            ]
            
            if not matching_files:
                print(f"No file matching '{filename}' found")
                return 1
            elif len(matching_files) == 1:
                category, filename = matching_files[0]
            else:
                print(f"Multiple files matching '{filename}':")
                category, filename = select_file_interactive(matching_files)
        elif filename and self.category:
            file_path = target_path / self.category / f"{filename.replace('.md', '')}.md"
            if not file_path.exists():
                print(f"File '{filename}' not found in category '{self.category}'")
                return 1
            category = self.category
        else:
            files = list_markdown_files(target_path, self.category)
            if not files:
                print("No markdown files found")
                return 1
            category, filename = select_file_interactive(files)
        
        if category:
            file_path = target_path / category / filename
        else:
            file_path = target_path / filename
        
        editor = self.editor or os.getenv('EDITOR')

        open_file_with_default_editor(file_path, editor)
        
        return 0