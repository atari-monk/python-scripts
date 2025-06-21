from pathlib import Path
import pyperclip
from plumbum import cli
from tool.blog.core.config_crud import ConfigCRUD
from tool.blog.core.cli import select_target_interactive
from tool.blog.core.text import clean_content


class SaveContent(cli.Application):
    
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
        target_path = select_target_interactive(config, target_name)
        
        if not self.category:
            self.category = input("Category path [e.g. 'tech/python']: ").strip()
        
        if not self.filename:
            self.filename = input("Filename (without extension): ").strip()
        
        full_path = target_path / self.category if self.category else target_path
        self._create_folder_if_not_exists(full_path)
        
        file_path = full_path / f"{self.filename}.md"
        print(f"\nReady to save to: {file_path}")
        
        with open(file_path, "a", encoding="utf-8") as f:
            while True:
                user_input = input("\nPress Enter to append clipboard (or 'q' to quit)... ")
                if user_input.lower() == 'q':
                    break
                
                content = pyperclip.paste().strip()
                if not content:
                    print("Clipboard is empty - nothing to append")
                    continue
                
                cleaned_content = clean_content(content)
                f.write(f"{cleaned_content}\n\n")
                print("✓ Appended (formatted)")
        
        print(f"\nDone. Content saved to: {file_path}")
        return 0