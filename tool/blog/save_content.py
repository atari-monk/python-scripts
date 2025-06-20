from plumbum import cli
from tool.blog.core.config_crud import ConfigCRUD
from pathlib import Path
import pyperclip
import os

from tool.blog.core.helper import select_target_interactive

class SaveContent(cli.Application):
    """Save clipboard content to a markdown file in the target repository"""
    
    category = cli.SwitchAttr(
        ['-c', '--category'],
        help="Category path (e.g. 'tech/python')"
    )
    
    filename = cli.SwitchAttr(
        ['-f', '--file'],
        help="Filename (without extension)"
    )
    
    def _create_folder_if_not_exists(self, path: Path) -> None:
        if not path.exists():
            path.mkdir(parents=True)
    
    def main(self, target_name: str = None):
        config = ConfigCRUD.load()
        
        # Select target
        try:
            target_path = select_target_interactive(config, target_name)
        except ValueError:
            return 1
        
        # Get category
        if not self.category:
            self.category = input(
                "Enter category path (e.g. 'tech/python' or leave empty): ").strip()
        
        # Get filename
        if not self.filename:
            self.filename = input(
                "Enter filename (without extension): ").strip()
        
        # Create full path
        full_path = target_path / self.category if self.category else target_path
        self._create_folder_if_not_exists(full_path)
        
        # Get content from clipboard
        input("Copy content to clipboard and press Enter...")
        content = pyperclip.paste()
        
        # Save to file
        file_path = full_path / f"{self.filename}.md"
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        
        print(f"Saved to: {file_path}")
        return 0