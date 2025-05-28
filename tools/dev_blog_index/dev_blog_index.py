from pathlib import Path

IGNORED_FILES = {'.prettierrc', 'index.md'}
IGNORED_DIRS = {'.git', 'page'}

class DevBlogIndex:
    def __init__(self, root_path='.'):
        self.root = Path(root_path)

    def generate(self):
        self._process_directory(self.root, is_root=True)

    def _process_directory(self, directory, is_root=False):
        if directory.name in IGNORED_DIRS:
            return

        subdirs = []
        markdown_files = []

        for item in directory.iterdir():
            if item.name in IGNORED_FILES:
                continue
            if item.is_dir() and item.name not in IGNORED_DIRS:
                subdirs.append(item)
            elif item.suffix == '.md' and item.name != 'index.md':
                markdown_files.append(item)

        if is_root:
            self._generate_root_index(directory, subdirs)
        elif subdirs or markdown_files:
            if subdirs and not markdown_files:
                self._generate_topic_index(directory, subdirs)
            else:
                self._generate_category_index(directory, markdown_files)

        for subdir in subdirs:
            self._process_directory(subdir)

    def _generate_root_index(self, directory, subdirs):
        content = [f"# {directory.name}\n"]
        for subdir in sorted(subdirs):
            content.append(f"- [{subdir.name}]({subdir.name}/index.md)")
        (directory / 'index.md').write_text('\n'.join(content))

    def _generate_topic_index(self, directory, subdirs):
        content = [f"# {directory.name}\n"]
        for subdir in sorted(subdirs):
            content.append(f"- [{subdir.name}]({subdir.name}/index.md)")
        (directory / 'index.md').write_text('\n'.join(content))

    def _generate_category_index(self, directory, markdown_files):
        content = [f"# {directory.name}\n"]
        for md_file in sorted(markdown_files):
            content.append(f"- [{md_file.stem}]({md_file.name})")
        (directory / 'index.md').write_text('\n'.join(content))