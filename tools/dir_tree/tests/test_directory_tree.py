import tempfile
import unittest
from pathlib import Path
from tools.dir_tree.directory_tree import DirectoryTree

class TestDirectoryTree(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.path = Path(self.temp_dir)
        
    def tearDown(self):
        for item in self.path.glob('**/*'):
            if item.is_file():
                item.unlink()
        for item in self.path.glob('*'):
            if item.is_dir():
                item.rmdir()
        self.path.rmdir()
        
    def test_ignores_specified_items(self):
        (self.path / ".git").mkdir()
        (self.path / "valid").mkdir()
        (self.path / "package-lock.json").touch()
        
        tree = DirectoryTree(self.temp_dir).generate()
        
        self.assertNotIn(".git", tree)
        self.assertNotIn("package-lock.json", tree)
        self.assertIn("valid", tree)
        
    def test_generates_correct_structure(self):
        (self.path / "dir1").mkdir()
        (self.path / "dir1/file1").touch()
        (self.path / "file2").touch()
        
        tree = DirectoryTree(self.temp_dir).generate()
        
        self.assertIn("dir1", tree)
        self.assertIn("file1", tree)
        self.assertIn("file2", tree)
        self.assertTrue(tree.startswith("#"))

if __name__ == "__main__":
    unittest.main()