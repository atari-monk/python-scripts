import pytest
import tempfile
from pathlib import Path
from core.dev_blog_index import DevBlogIndex

@pytest.fixture
def sample_blog_structure():
    with tempfile.TemporaryDirectory() as tmpdir:
        root = Path(tmpdir)
        (root / ".prettierrc").touch()
        (root / "_config.yml").touch()
        (root / "blog_metadata.json").touch()
        (root / "python").mkdir()
        (root / "python" / "environments").mkdir()
        (root / "python" / "environments" / "virtual-environments.md").touch()
        (root / "python" / "json").mkdir()
        (root / "python" / "json" / "json-and-pydantic.md").touch()
        (root / "python" / "json" / "json-data-loading-utility.md").touch()
        (root / "python" / "json" / "loading-objects-from-json.md").touch()
        yield root

def test_generate_root_index(sample_blog_structure):
    generator = DevBlogIndex(sample_blog_structure)
    generator.generate()
    root_index = sample_blog_structure / "index.md"
    assert root_index.exists()
    content = root_index.read_text()
    assert "# Dev Blog" in content
    assert "[python](python/index.md)" in content

def test_generate_topic_index(sample_blog_structure):
    generator = DevBlogIndex(sample_blog_structure)
    generator.generate()
    topic_index = sample_blog_structure / "python" / "index.md"
    assert topic_index.exists()
    content = topic_index.read_text()
    assert "# python" in content
    assert "[environments](environments/index.md)" in content
    assert "[json](json/index.md)" in content

def test_generate_category_index(sample_blog_structure):
    generator = DevBlogIndex(sample_blog_structure)
    generator.generate()
    category_index = sample_blog_structure / "python" / "json" / "index.md"
    assert category_index.exists()
    content = category_index.read_text()
    assert "# json" in content
    assert "[json-and-pydantic](json-and-pydantic.md)" in content
    assert "[json-data-loading-utility](json-data-loading-utility.md)" in content

def test_ignore_files_and_folders(sample_blog_structure):
    generator = DevBlogIndex(sample_blog_structure)
    generator.generate()
    assert not (sample_blog_structure / "_layouts" / "index.md").exists()
    assert not (sample_blog_structure / "assets" / "index.md").exists()
    assert not (sample_blog_structure / "docs" / "index.md").exists()