import json
import pyperclip
from datetime import datetime
import re
from pathlib import Path

class DevBlogPost:
    def __init__(self, config_path=None):
        self.config_path = Path(config_path) if config_path else Path.home() / ".dev_blog_config.json"
        self.config = None
        self.load_or_initialize_config()

    def load_or_initialize_config(self):
        if self.config_path.exists():
            with open(self.config_path, 'r') as f:
                self.config = json.load(f)
        else:
            self.config = {
                "repo_path": "",
                "current_content": "posts",
                "current_category": "uncategorized"
            }

    def save_config(self):
        self.config_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.config_path, 'w') as f:
            json.dump(self.config, f, indent=2)

    def slugify(self, text):
        text = text.lower().strip()
        text = re.sub(r'[^\w\s-]', '', text)
        text = re.sub(r'[\s_-]+', '-', text)
        return re.sub(r'^-+|-+$', '', text)

    def get_next_filename(self, category_path, title):
        base_name = self.slugify(title) + ".md"
        counter = 1
        while (category_path / base_name).exists():
            base_name = f"{self.slugify(title)}-{counter}.md"
            counter += 1
        return base_name

    def update_metadata(self, post_title, post_filename):
        repo_path = Path(self.config["repo_path"])
        repo_path.mkdir(parents=True, exist_ok=True)
        metadata_path = repo_path / "blog_metadata.json"
        
        if metadata_path.exists():
            with open(metadata_path, 'r') as f:
                metadata = json.load(f)
        else:
            metadata = {"posts": []}
        
        metadata["posts"].append({
            "title": post_title,
            "filename": post_filename,
            "category": self.config["current_category"],
            "content": self.config["current_content"],
            "created": datetime.now().isoformat(),
            "path": f"{self.config['current_content']}/{self.config['current_category']}/{post_filename}"
        })
        
        with open(metadata_path, 'w') as f:
            json.dump(metadata, f, indent=2)

    def process_clipboard_content(self):
        markdown_content = pyperclip.paste().strip()
        if not markdown_content:
            raise ValueError("Clipboard is empty")

        normalized_content = '\n'.join(line.rstrip() for line in markdown_content.splitlines())
        first_line = normalized_content.split('\n')[0]
        post_title = first_line.lstrip('#').strip() if first_line.startswith('#') else "Untitled Post"

        repo_path = Path(self.config["repo_path"])
        category_path = repo_path / self.config["current_content"] / self.config["current_category"]
        category_path.mkdir(parents=True, exist_ok=True)

        post_filename = self.get_next_filename(category_path, post_title)
        post_path = category_path / post_filename
        
        post_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(post_path, 'w', encoding='utf-8') as f:
            f.write(normalized_content)
        
        self.update_metadata(post_title, post_filename)
        return str(post_path)