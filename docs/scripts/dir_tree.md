# Copy File System Tree to clipboard Script 

Directory Tree

- Assumptions:
  - Ask questions if something is unclear
  - Tell if you have simpler idea
  - Write so that even machine can use this code
  - Simpliffy as much as possible
- Development:
  - Use python
  - No comments, self-documenting code only
  - Write pytest unit tests first
  - Implement class to pass tests
  - Implement script to use class in CLI
  - CLI script in separate file
  - For CLI use argparse
- Functionality:
  - Prints file system tree to md
- Stores it in clipboard and optionally stores to md file
- Check my current implementation  
- Files:
  ```python
import os

IGNORE = {
    "folders": {".git", "node_modules", "dist", "__pycache__", "venv", ".venv", "env", "my_scripts.egg-info", ".pytest_cache"},
    "files": {"package-lock.json"}
}

class DirectoryTreeGenerator:
    def __init__(self, root_path: str):
        self.root_path = os.path.normpath(root_path)
        self.repo_name = os.path.basename(self.root_path)
        
    def generate(self) -> str:
        structure = self._generate_structure(self.root_path)
        return f"# File Tree of repository `{self.repo_name}`\n\n```\n{structure}\n```"
    
    def _generate_structure(self, path: str, prefix: str = "") -> str:
        try:
            items = sorted(os.listdir(path))
        except PermissionError:
            return f"{prefix}└── [Permission denied]\n"
            
        output = []
        filtered_items = [item for item in items if not self._should_ignore(os.path.join(path, item), item)]
        
        for i, item in enumerate(filtered_items):
            full_path = os.path.join(path, item)
            is_last = i == len(filtered_items) - 1
            line = prefix + ("└── " if is_last else "├── ") + item
            output.append(line)
            
            if os.path.isdir(full_path):
                new_prefix = prefix + ("    " if is_last else "│   ")
                subtree = self._generate_structure(full_path, new_prefix)
                if subtree.strip():
                    output.append(subtree)
        
        return "\n".join(output)
    
    def _should_ignore(self, full_path: str, item: str) -> bool:
        if os.path.isdir(full_path) and item in IGNORE["folders"]:
            return True
        if os.path.isfile(full_path) and item in IGNORE["files"]:
            return True
        return False
```

```python
import os
import logging
from pathlib import Path
from typing import Optional
import pyperclip
from core.directory_tree_generator import DirectoryTreeGenerator

DEFAULT_ENCODING = "utf-8"
DEFAULT_DOCS_DIR = "docs"
OUTPUT_FILENAME_TEMPLATE = "{repo_name}_file_tree.md"

class DirectoryTreeProvider:
    def __init__(self, log_level=logging.INFO):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(log_level)

    def validate_directory(self, path: str) -> bool:
        return os.path.isdir(path)

    def save_to_file(self, content: str, directory: str, filename: str) -> str:
        Path(directory).mkdir(parents=True, exist_ok=True)
        output_path = os.path.join(directory, filename)

        with open(output_path, "w", encoding=DEFAULT_ENCODING) as f:
            f.write(content)

        return output_path

    def generate_tree(self, path: str, save: bool = False, output_dir: str = DEFAULT_DOCS_DIR) -> Optional[str]:
        if not self.validate_directory(path):
            self.logger.error("Invalid directory path")
            return None

        try:
            generator = DirectoryTreeGenerator(path)
            md_content = generator.generate()

            try:
                pyperclip.copy(md_content)
                self.logger.info("Structure copied to clipboard!")
            except pyperclip.PyperclipException as e:
                self.logger.warning(f"Could not copy to clipboard - {str(e)}")

            if save:
                output_filename = OUTPUT_FILENAME_TEMPLATE.format(
                    repo_name=generator.repo_name
                )
                output_path = self.save_to_file(
                    md_content,
                    os.path.join(path, output_dir),
                    output_filename
                )
                self.logger.info(f"Saved to {output_path}")
                return output_path

            return md_content

        except Exception as e:
            self.logger.error(f"Error: {str(e)}")
            raise
```

```python
import argparse
import logging
from core.directory_tree_provider import DEFAULT_DOCS_DIR, DirectoryTreeProvider

def main():
    logging.basicConfig(level=logging.INFO)
    parser = argparse.ArgumentParser()
    parser.add_argument("path", help="Directory path to generate structure for")
    parser.add_argument("-s", "--save", action="store_true", help="Save to markdown file")
    parser.add_argument("-o", "--output-dir", default=DEFAULT_DOCS_DIR, help="Output directory")
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose logging")
    args = parser.parse_args()

    generator = DirectoryTreeProvider(log_level=logging.DEBUG if args.verbose else logging.INFO)
    generator.generate_tree(args.path, args.save, args.output_dir)

if __name__ == "__main__":
    main()
```

```python
import os
import tempfile
import unittest
from core.directory_tree_generator import IGNORE, DirectoryTreeGenerator

class TestDirectoryTreeGenerator(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.repo_name = os.path.basename(self.test_dir)

    def tearDown(self):
        for root, dirs, files in os.walk(self.test_dir, topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
            for name in dirs:
                os.rmdir(os.path.join(root, name))
        os.rmdir(self.test_dir)

    def _create_test_files(self, structure):
        for name, content in structure.items():
            path = os.path.join(self.test_dir, name)
            if content is None:
                os.makedirs(path, exist_ok=True)
            else:
                with open(path, 'w') as f:
                    f.write(content)

    def test_ignore_files(self):
        structure = {
            "included.txt": "content",
            "package-lock.json": "{}"
        }
        self._create_test_files(structure)
        
        generator = DirectoryTreeGenerator(self.test_dir)
        result = generator.generate()
        
        self.assertIn("included.txt", result)
        self.assertNotIn("package-lock.json", result)

    def test_ignore_folders(self):
        structure = {
            "included_dir": None,
            ".git": None,
            "node_modules": None,
            "included_dir/file.txt": "content"
        }
        self._create_test_files(structure)
        
        generator = DirectoryTreeGenerator(self.test_dir)
        result = generator.generate()
        
        self.assertIn("included_dir", result)
        self.assertIn("file.txt", result)
        self.assertNotIn(".git", result)
        self.assertNotIn("node_modules", result)

    def test_should_ignore_folder(self):
        generator = DirectoryTreeGenerator(self.test_dir)
        for folder in IGNORE["folders"]:
            path = os.path.join(self.test_dir, folder)
            os.makedirs(path, exist_ok=True)
            self.assertTrue(generator._should_ignore(path, folder))

    def test_should_ignore_file(self):
        generator = DirectoryTreeGenerator(self.test_dir)
        for file in IGNORE["files"]:
            path = os.path.join(self.test_dir, file)
            with open(path, 'w') as f:
                f.write("test")
            self.assertTrue(generator._should_ignore(path, file))

if __name__ == '__main__':
    unittest.main()
```