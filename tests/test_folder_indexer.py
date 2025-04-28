import pytest
from unittest.mock import MagicMock, mock_open, patch
import logging
from core.folder_indexer import FolderIndexer

class TestFolderIndexer:
    @pytest.fixture
    def mock_logger(self):
        logger = MagicMock(spec=logging.Logger)
        return logger

    @pytest.fixture
    def temp_repo_path(self, tmp_path):
        repo_path = tmp_path / "test_repo"
        repo_path.mkdir()
        return repo_path

    def test_init_with_valid_path(self, temp_repo_path, mock_logger):
        generator = FolderIndexer(temp_repo_path, mock_logger)
        assert generator.repo_path == temp_repo_path.resolve()
        mock_logger.assert_not_called()

    def test_init_with_invalid_path_raises_filenotfounderror(self, mock_logger):
        with pytest.raises(FileNotFoundError):
            FolderIndexer("/nonexistent/path", mock_logger)

    def test_init_with_file_path_raises_notadirectoryerror(self, temp_repo_path, mock_logger):
        file_path = temp_repo_path / "test_file"
        file_path.touch()
        with pytest.raises(NotADirectoryError):
            FolderIndexer(file_path, mock_logger)

    def test_clean_name(self):
        assert FolderIndexer.clean_name("test_name") == "Test Name"
        assert FolderIndexer.clean_name("test-name") == "Test Name"
        assert FolderIndexer.clean_name("  test_name  ") == "Test Name"
        assert FolderIndexer.clean_name("TEST_NAME") == "Test Name"

    def test_determine_base_path_with_docs_dir(self, temp_repo_path, mock_logger):
        docs_path = temp_repo_path / "docs"
        docs_path.mkdir()
        generator = FolderIndexer(temp_repo_path, mock_logger)
        base_path, index_file = generator.determine_base_path()
        assert base_path == docs_path
        assert index_file == docs_path / "index.md"

    def test_determine_base_path_without_docs_dir(self, temp_repo_path, mock_logger):
        generator = FolderIndexer(temp_repo_path, mock_logger)
        base_path, index_file = generator.determine_base_path()
        assert base_path == temp_repo_path
        assert index_file == temp_repo_path / "index.md"

    def test_scan_directory_returns_correct_files(self, temp_repo_path, mock_logger):
        subdir = temp_repo_path / "subdir"
        subdir.mkdir()
        md_file = temp_repo_path / "test.md"
        md_file.touch()
        other_file = temp_repo_path / "test.txt"
        other_file.touch()

        generator = FolderIndexer(temp_repo_path, mock_logger)
        subdirs, md_files = generator.scan_directory(temp_repo_path)

        assert subdirs == [subdir]
        assert md_files == [md_file]
        mock_logger.assert_not_called()

    def test_scan_directory_logs_permission_error(self, temp_repo_path, mock_logger):
        with patch('os.scandir') as mock_scandir:
            mock_scandir.return_value.__enter__.return_value = [MagicMock(is_dir=lambda: True)]
            mock_scandir.side_effect = PermissionError("Permission denied")
            
            generator = FolderIndexer(temp_repo_path, mock_logger)
            subdirs, md_files = generator.scan_directory(temp_repo_path)
            
            assert subdirs == []
            assert md_files == []
            mock_logger.warning.assert_called_once()

    def test_generate_section_content(self, temp_repo_path, mock_logger):
        section_path = temp_repo_path / "section"
        section_path.mkdir()
        md_file = section_path / "test.md"
        md_file.touch()

        generator = FolderIndexer(temp_repo_path, mock_logger)
        content = generator.generate_section_content(temp_repo_path, section_path)

        assert content == ["\n## Section", "- [Test](section/test.md)"]

    def test_generate_index_content_with_files_in_root(self, temp_repo_path, mock_logger):
        md_file = temp_repo_path / "test.md"
        md_file.touch()

        generator = FolderIndexer(temp_repo_path, mock_logger)
        content = generator.generate_index_content(temp_repo_path)

        assert content == ["\n## Documentation Index\n", "- [Test](test.md)"]

    def test_generate_index_content_with_subdirs(self, temp_repo_path, mock_logger):
        section_path = temp_repo_path / "section"
        section_path.mkdir()
        md_file = section_path / "test.md"
        md_file.touch()

        generator = FolderIndexer(temp_repo_path, mock_logger)
        content = generator.generate_index_content(temp_repo_path)

        assert content == ["\n## Documentation Index\n","\n## Section", "- [Test](section/test.md)"]

    def test_write_index_file_success(self, temp_repo_path, mock_logger):
        index_file = temp_repo_path / "index.md"
        content = ["# Test", "Content"]

        generator = FolderIndexer(temp_repo_path, mock_logger)
        with patch('builtins.open', mock_open()) as mock_file:
            generator.write_index_file(index_file, content)
            
        mock_file.assert_called_once_with(index_file, 'w', encoding='utf-8')
        mock_logger.info.assert_called_once()

    def test_write_index_file_failure(self, temp_repo_path, mock_logger):
        index_file = temp_repo_path / "index.md"
        content = ["# Test", "Content"]

        generator = FolderIndexer(temp_repo_path, mock_logger)
        with patch('builtins.open', side_effect=IOError("Failed to write")):
            with pytest.raises(IOError):
                generator.write_index_file(index_file, content)
                
        mock_logger.error.assert_called_once()

    def test_generate_success(self, temp_repo_path, mock_logger):
        docs_path = temp_repo_path / "docs"
        docs_path.mkdir()
        section_path = docs_path / "section"
        section_path.mkdir()
        md_file = section_path / "test.md"
        md_file.touch()

        generator = FolderIndexer(temp_repo_path, mock_logger)
        with patch.object(generator, 'write_index_file') as mock_write:
            generator.generate()
            
        mock_write.assert_called_once()