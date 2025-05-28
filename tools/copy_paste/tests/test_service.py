import os
from tempfile import TemporaryDirectory
from unittest.mock import patch
from core.copy_paste_config import CopyPasteConfig
from tools.copy_paste.service import CopyPasteService

class TestCopyPasteService:
    @patch('builtins.input', side_effect=['file1.py', 'file2.py'])
    @patch('pyperclip.paste', side_effect=['content1', 'content2'])
    def test_paste_to_all_entries(self, mock_paste, mock_input):
        with TemporaryDirectory() as tmpdir1, TemporaryDirectory() as tmpdir2:
            config_path = os.path.join(tmpdir1, 'config.json')
            config = CopyPasteConfig(config_path)
            config.add_profile('dev', [
                {'path': tmpdir1, 'category': 'backend'},
                {'path': tmpdir2, 'category': 'frontend'}
            ])
            config.set_current_key('dev')
            
            manager = CopyPasteService(config)
            manager.paste_to_all_entries()
            
            with open(os.path.join(tmpdir1, 'file1.py'), 'r') as f:
                assert f.read() == 'content1'
            with open(os.path.join(tmpdir2, 'file2.py'), 'r') as f:
                assert f.read() == 'content2'