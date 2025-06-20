from plumbum import cli
from tool.blog.core.config_crud import ConfigCRUD
from pathlib import Path
import pyperclip
import os

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
    
    def _select_target(self, config, target_name: str = None) -> Path:
        if target_name and target_name in config.targets:
            path = config.targets[target_name]
            if not path:
                path = input(f"Enter path for target '{target_name}': ").strip()
                config.targets[target_name] = path
                ConfigCRUD.save(config)
            return Path(path).resolve()
        
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
                    path = config.targets[selected_name]
                    if not path:
                        path = input(f"Enter path for {selected_name}: ").strip()
                        config.targets[selected_name] = path
                        ConfigCRUD.save(config)
                    return Path(path).resolve()
            except ValueError:
                pass
            print("Invalid selection, please try again")
    
    def main(self, target_name: str = None):
        config = ConfigCRUD.load()
        
        # Select target
        target_path = self._select_target(config, target_name)
        
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