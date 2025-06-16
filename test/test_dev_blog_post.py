import pytest
from unittest.mock import patch
from pathlib import Path
import json
from datetime import datetime
from tool.dev_blog_post.dev_blog_post import DevBlogPost

@pytest.fixture
def mock_config():
    return {
        "repo_path": "/test/repo",
        "current_content": "content",
        "current_category": "category"
    }

@pytest.fixture
def mock_post():
    return {
        "title": "Test Post",
        "filename": "test-post.md",
        "category": "category",
        "content": "content",
        "created": datetime.now().isoformat(),
        "path": "content/category/test-post.md"
    }

def test_slugify():
    blog = DevBlogPost()
    assert blog.slugify("Hello World!") == "hello-world"
    assert blog.slugify("Test--Post 123") == "test-post-123"
    assert blog.slugify("  Trim Me  ") == "trim-me"

def test_get_next_filename(tmp_path, mock_config):
    blog = DevBlogPost()
    blog.config = mock_config
    
    category_path = tmp_path / "content" / "category"
    category_path.mkdir(parents=True)
    
    assert blog.get_next_filename(category_path, "Test") == "test.md"
    
    (category_path / "test.md").touch()
    assert blog.get_next_filename(category_path, "Test") == "test-1.md"
    
    (category_path / "test-1.md").touch()
    assert blog.get_next_filename(category_path, "Test") == "test-2.md"

def test_update_metadata(tmp_path, mock_config, mock_post):
    blog = DevBlogPost()
    blog.config = mock_config
    blog.config["repo_path"] = str(tmp_path)
    
    metadata_file = tmp_path / "blog_metadata.json"
    metadata_file.write_text('{"posts": []}')
    
    blog.update_metadata("Test Post", "test-post.md")
    
    with open(metadata_file) as f:
        metadata = json.load(f)
        assert len(metadata["posts"]) == 1
        assert metadata["posts"][0]["title"] == "Test Post"
        assert metadata["posts"][0]["filename"] == "test-post.md"

    blog.update_metadata("Second Post", "second-post.md")
    
    with open(metadata_file) as f:
        metadata = json.load(f)
        assert len(metadata["posts"]) == 2
        assert metadata["posts"][1]["title"] == "Second Post"

def test_process_clipboard_content(tmp_path, mock_config):
    blog = DevBlogPost()
    blog.config = {
        "repo_path": str(tmp_path),
        "current_content": "content",
        "current_category": "category"
    }
    
    test_content = "# Test Post\n\nContent"
    with patch('pyperclip.paste', return_value=test_content):
        saved_path = blog.process_clipboard_content()
        
        expected_path = tmp_path / "content" / "category" / "test-post.md"
        assert Path(saved_path) == expected_path
        assert expected_path.exists()
        
        with open(expected_path, 'r', encoding='utf-8') as f:
            assert f.read() == test_content
        
        metadata_path = tmp_path / "blog_metadata.json"
        assert metadata_path.exists()
        with open(metadata_path, 'r') as f:
            metadata = json.load(f)
            assert len(metadata["posts"]) == 1
            assert metadata["posts"][0]["title"] == "Test Post"