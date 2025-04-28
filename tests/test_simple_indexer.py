import pytest
import tempfile
import shutil
from pathlib import Path
from core.simple_indexer import SimpleFolderIndexer

@pytest.fixture
def test_folder():
    test_dir = Path(tempfile.mkdtemp())
    (test_dir / "subdir").mkdir()
    (test_dir / "file1.md").touch()
    (test_dir / "subdir" / "file2.md").touch()
    (test_dir / "ignore.txt").touch()
    yield test_dir
    shutil.rmtree(test_dir)

def test_generate_creates_index_file(test_folder):
    indexer = SimpleFolderIndexer(str(test_folder))
    indexer.generate()
    assert (test_folder / "index.md").exists()

def test_index_content_format(test_folder):
    indexer = SimpleFolderIndexer(str(test_folder))
    indexer.generate()
    content = (test_folder / "index.md").read_text()
    assert "# Documentation Index" in content
    assert "- [File1](file1.md)" in content
    assert "- [File2](subdir\\file2.md)" in content
    assert "ignore.txt" not in content

def test_overwrites_existing_index(test_folder):
    (test_folder / "index.md").write_text("old content")
    indexer = SimpleFolderIndexer(str(test_folder))
    indexer.generate()
    content = (test_folder / "index.md").read_text()
    assert content.startswith("# Documentation Index")
    assert "old content" not in content