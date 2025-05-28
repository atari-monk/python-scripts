import os
from pathlib import Path
from typing import List, Tuple, Union
from logging import Logger

class FolderIndexer:
    def __init__(self, repo_path: Union[str, Path], logger: Logger):
        self.repo_path = Path(repo_path).resolve()
        self.validate_path()
        self.logger = logger

    def validate_path(self) -> None:
        if not self.repo_path.exists():
            raise FileNotFoundError(f"Repository path does not exist: {self.repo_path}")
        if not self.repo_path.is_dir():
            raise NotADirectoryError(f"Repository path is not a directory: {self.repo_path}")

    @staticmethod
    def clean_name(name: str) -> str:
        return name.replace('_', ' ').replace('-', ' ').title().strip()

    def determine_base_path(self) -> Tuple[Path, Path]:
        docs_path = self.repo_path / 'docs'

        if docs_path.exists() and docs_path.is_dir():
            return docs_path, docs_path / 'index.md'
        return self.repo_path, self.repo_path / 'index.md'

    def scan_directory(self, path: Path) -> Tuple[List[Path], List[Path]]:
        subdirs = []
        md_files = []

        try:
            with os.scandir(path) as entries:
                for entry in entries:
                    if entry.is_dir():
                        subdirs.append(Path(entry.path))
                    elif (entry.is_file() and
                          entry.name.lower().endswith('.md') and
                          entry.name.lower() != 'index.md'):
                        md_files.append(Path(entry.path))
        except PermissionError as e:
            self.logger.warning(f"Permission denied scanning directory {path}: {e}")
        except OSError as e:
            self.logger.error(f"Error scanning directory {path}: {e}")
            raise

        return subdirs, md_files

    def generate_section_content(self, base_path: Path, path: Path) -> List[str]:
        content = []
        _, md_files = self.scan_directory(path)

        if not md_files:
            return content

        rel_path = path.relative_to(base_path)
        section_name = self.clean_name(rel_path.name)
        content.append(f"\n## {section_name}")

        for file in sorted(md_files):
            name = self.clean_name(file.stem)
            rel_file_path = file.relative_to(base_path)
            content.append(f"- [{name}]({str(rel_file_path).replace('\\', '/')})")

        return content

    def generate_index_content(self, base_path: Path) -> List[str]:
        content = []
        subdirs, md_files = self.scan_directory(base_path)

        content.append("\n## Documentation Index\n")

        if md_files:
            for file in sorted(md_files):
                name = self.clean_name(file.stem)
                content.append(f"- [{name}]({file.name})")

        for root in sorted(subdirs):
            section_content = self.generate_section_content(base_path, root)
            content.extend(section_content)

        return content

    def write_index_file(self, index_file: Path, content: List[str]) -> None:
        try:
            with open(index_file, 'w', encoding='utf-8') as f:
                f.write('\n'.join(content))
            self.logger.info(f"Successfully generated index with {len(content) - 1} sections in {index_file}")
        except IOError as e:
            self.logger.error(f"Failed to write index file {index_file}: {e}")
            raise

    def generate(self) -> None:
        try:
            base_path, index_file = self.determine_base_path()
            content = self.generate_index_content(base_path)
            self.write_index_file(index_file, content)
        except Exception as e:
            self.logger.error(f"Failed to generate documentation index: {e}")
            raise