import argparse
import os
from tool.copy_paste.config import CopyPasteConfig
from tool.copy_paste.service import CopyPasteService

DEFAULT_CONFIG_PATH = os.path.expanduser(r'C:\atari-monk\code\apps-data-store\paste_code_config.json')

def setup_config(config_path):
    config = CopyPasteConfig(config_path)
    
    print("No profiles configured. Let's create one.")
    while True:
        key = input("Enter profile key (name): ")
        entries = []
        while True:
            path = input("Enter target path: ")
            category = input("Enter category: ")
            entries.append({'path': path, 'category': category})
            
            another_entry = input("Add another path-category to this profile? (y/n): ").lower()
            if another_entry != 'y':
                break
        
        config.add_profile(key, entries)
        config.set_current_key(key)
        
        another_profile = input("Add another profile? (y/n): ").lower()
        if another_profile != 'y':
            break
    
    return config

def list_profiles(config):
    profiles = config.get_all_profiles()
    if not profiles:
        print("No profiles available")
        return
    
    current_key = config.get_current_key()
    for key, entries in profiles.items():
        status = " (current)" if key == current_key else ""
        print(f"{key}{status}:")
        for entry in entries:
            print(f"  - path={entry['path']}, category={entry['category']}")

def main():
    parser = argparse.ArgumentParser(description='Paste code from clipboard to files')
    parser.add_argument('--config', help='Config file path', default=DEFAULT_CONFIG_PATH)
    parser.add_argument('--list', help='List all profiles', action='store_true')
    parser.add_argument('--set-current', help='Set current profile')
    args = parser.parse_args()

    config = CopyPasteConfig(args.config)
    
    if args.list:
        list_profiles(config)
        return
    
    if args.set_current:
        if args.set_current in config.get_all_profiles():
            config.set_current_key(args.set_current)
            print(f"Current profile set to: {args.set_current}")
        else:
            print(f"Profile {args.set_current} not found")
        return
    
    if not config.get_current_key():
        config = setup_config(args.config)
    
    manager = CopyPasteService(config)
    manager.paste_to_all_entries()

if __name__ == '__main__':
    main()