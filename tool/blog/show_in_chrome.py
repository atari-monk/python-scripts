from plumbum import cli
import os
import subprocess
from pathlib import Path
from tool.blog.core.config_crud import ConfigCRUD
from tool.blog.core.cli import select_target_interactive
from tool.blog.core.file_sys import list_markdown_files, select_file_interactive


class ShowInChrome(cli.Application):
    """Open markdown file directly in Chrome browser"""
    
    category = cli.SwitchAttr(
        ['-c', '--category'],
        help="Category path (e.g. 'tech/python')"
    )
    
    def main(self, target_name: str = None, filename: str = None):
        config = ConfigCRUD.load()
        
        try:
            target_path = select_target_interactive(config, target_name)
        except ValueError:
            return 1
        
        # Get the markdown file
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
            if not files:
                print("No markdown files found")
                return 1
            category, filename = select_file_interactive(files)
        
        # Get full path to markdown file
        if category:
            md_file = target_path / category / filename
        else:
            md_file = target_path / filename
        
        # Open in Chrome
        self._open_in_chrome(md_file)
        
        return 0
    
    def _open_in_chrome(self, md_file: Path):
        """Open markdown file directly in Chrome"""
        chrome_path = self._find_chrome_path()
        
        if chrome_path:
            try:
                # Use file:// URI to open the local file
                subprocess.run([chrome_path, f"file://{md_file.resolve()}"])
                print(f"Opening {md_file.name} in Chrome...")
            except Exception as e:
                print(f"Error opening Chrome: {e}")
        else:
            print("Chrome not found - trying default browser")
            import webbrowser
            webbrowser.open(f"file://{md_file.resolve()}")
    
    def _find_chrome_path(self) -> str:
        """Find Chrome executable path for different platforms"""
        if os.name == 'nt':  # Windows
            paths = [
                'C:/Program Files/Google/Chrome/Application/chrome.exe',
                'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe',
                os.path.expanduser('~') + '/AppData/Local/Google/Chrome/Application/chrome.exe'
            ]
        elif os.name == 'posix':  # macOS or Linux
            paths = [
                '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',  # macOS
                '/usr/bin/google-chrome',  # Linux common path
                '/usr/bin/chromium-browser',
                'google-chrome'  # Try via PATH
            ]
        
        for path in paths:
            if os.path.exists(path):
                return path
        return None