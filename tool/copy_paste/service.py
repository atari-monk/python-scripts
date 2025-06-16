import os
import pyperclip

class CopyPasteService:
    def __init__(self, config):
        self.config = config

    def paste_to_all_entries(self):
        entries = self.config.get_current_profile_entries()
        if not entries:
            raise ValueError("No entries in current profile")
        
        for entry in entries:
            filename = input(f"Enter filename for {entry['category']} ({entry['path']}): ")
            file_path = os.path.join(entry['path'], filename)
            
            if os.path.exists(file_path):
                overwrite = input(f"File {filename} exists. Overwrite? (y/n): ").lower()
                if overwrite != 'y':
                    continue
            
            print(f"Paste content for {filename} and press Enter...")
            content = pyperclip.paste().strip()
            if not content:
                raise ValueError("Clipboard is empty")
            normalized_content = '\n'.join(line.rstrip() for line in content.splitlines())
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(normalized_content)
            print(f"Saved to {file_path}")