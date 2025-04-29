import os
from tempfile import TemporaryDirectory
from core.copy_paste_config import CopyPasteConfig

class TestCopyPasteConfig:
    def test_add_and_get_config(self):
        with TemporaryDirectory() as tmpdir:
            config_path = os.path.join(tmpdir, 'config.json')
            config = CopyPasteConfig(config_path)
            
            config.add_profile('dev', [
                {'path': '/dev/path1', 'category': 'backend'},
                {'path': '/dev/path2', 'category': 'frontend'}
            ])
            
            assert config.get_profile_entries('dev') == [
                {'path': '/dev/path1', 'category': 'backend'},
                {'path': '/dev/path2', 'category': 'frontend'}
            ]
            
            config.set_current_key('dev')
            assert config.get_current_key() == 'dev'
            
            assert config.get_current_profile_entries() == [
                {'path': '/dev/path1', 'category': 'backend'},
                {'path': '/dev/path2', 'category': 'frontend'}
            ]