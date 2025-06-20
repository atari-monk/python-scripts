from plumbum import cli
from tool.blog.core.config_crud import ConfigCRUD
from pathlib import Path
import os
import subprocess
import sys

from tool.blog.core.helper import select_target_interactive

class OpenFile(cli.Application):
    """Open a markdown file from the target repository"""
    
    category = cli.SwitchAttr(
        ['-c', '--category'],
        help="Category path (e.g. 'tech/python')"
    )
    
    editor = cli.SwitchAttr(
        ['-e', '--editor'],
        help="Specify editor command (default: system default)"
    )
    
    def _find_files(self, target_path: Path, category: str = None) -> list:
        """Find all markdown files in the target"""
        files = []
        search_path = target_path / category if category else target_path
        
        if not search_path.exists():
            return []
            
        for item in search_path.glob('**/*.md'):
            rel_path = os.path.relpath(item.parent, target_path)
            if rel_path == '.':
                file_category = ''
            else:
                file_category = rel_path.replace("\\", "/")
            files.append((file_category, item.name))
        
        return sorted(files, key=lambda x: (x[0], x[1]))
    
    def _select_file(self, files: list) -> tuple:
        """Interactive file selection"""
        print("\nAvailable files:")
        for i, (category, filename) in enumerate(files, 1):
            display_category = f"[{category}] " if category else ""
            print(f"{i}. {display_category}{filename}")
        
        while True:
            choice = input("\nSelect file (1-{}): ".format(
                len(files))).strip()
            
            try:
                choice_num = int(choice)
                if 1 <= choice_num <= len(files):
                    return files[choice_num-1]
            except ValueError:
                pass
            print("Invalid selection, please try again")
    
    def main(self, target_name: str = None, filename: str = None):
        config = ConfigCRUD.load()
        
        try:
            target_path = select_target_interactive(config, target_name)
        except ValueError:
            return 1
        
        # If filename specified but no category, search all categories
        if filename and not self.category:
            files = self._find_files(target_path)
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
                category, filename = self._select_file(matching_files)
        elif filename and self.category:
            # Verify file exists
            file_path = target_path / self.category / f"{filename.replace('.md', '')}.md"
            if not file_path.exists():
                print(f"File '{filename}' not found in category '{self.category}'")
                return 1
            category = self.category
        else:
            # Interactive mode - find and select file
            files = self._find_files(target_path, self.category)
            if not files:
                print("No markdown files found")
                return 1
            category, filename = self._select_file(files)
        
        # Determine full path
        if category:
            file_path = target_path / category / filename
        else:
            file_path = target_path / filename
        
        # Open file
        editor = self.editor or os.getenv('EDITOR')
        try:
            if editor:
                subprocess.run([editor, file_path], check=True)
            elif sys.platform == 'win32':
                os.startfile(file_path)
            elif sys.platform == 'darwin':
                subprocess.run(['open', file_path], check=True)
            else:
                subprocess.run(['xdg-open', file_path], check=True)
        except Exception as e:
            print(f"Failed to open file: {e}")
            return 1
        
        return 0