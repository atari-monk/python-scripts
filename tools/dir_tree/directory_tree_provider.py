import os
import logging
from pathlib import Path
from typing import Optional
import pyperclip
from tools.dir_tree.directory_tree import DirectoryTreeGenerator

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