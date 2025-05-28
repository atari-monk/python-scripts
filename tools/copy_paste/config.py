import os
import json

class CopyPasteConfig:
    def __init__(self, config_path):
        if not isinstance(config_path, (str, bytes, os.PathLike)):
            raise TypeError("config_path must be a string or path-like object")
        self.config_path = config_path
        if not os.path.exists(self.config_path):
            self._save_config({
                'profiles': {},
                'current_key': None
            })

    def _load_config(self):
        with open(self.config_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def _save_config(self, config):
        with open(self.config_path, 'w') as f:
            json.dump(config, f, indent=2)

    def add_profile(self, key, entries):
        config = self._load_config()
        config['profiles'][key] = entries
        self._save_config(config)

    def get_profile_entries(self, key):
        return self._load_config()['profiles'].get(key, [])

    def get_all_profiles(self):
        return self._load_config()['profiles']

    def set_current_key(self, key):
        config = self._load_config()
        config['current_key'] = key
        self._save_config(config)

    def get_current_key(self):
        return self._load_config()['current_key']

    def get_current_profile_entries(self):
        key = self.get_current_key()
        if key:
            return self.get_profile_entries(key)
        return []