from plumbum import cli
from pathlib import Path
import os
from tool.blog.core.config_crud import ConfigCRUD
from tool.blog.core.cli import select_target_interactive
from tool.blog.core.file_sys import list_markdown_files, select_file_interactive


class DeleteFile(cli.Application):
    """Delete a markdown file from the blog"""
    
    category = cli.SwitchAttr(
        ['-c', '--category'],
        help="Category path (e.g. 'tech/python')"
    )
    
    force = cli.Flag(
        ['-f', '--force'],
        help="Delete without confirmation"
    )
    
    def main(self, target_name: str = None, filename: str = None):
        config = ConfigCRUD.load()
        
        try:
            target_path = select_target_interactive(config, target_name)
        except ValueError:
            return 1
        
        # Get the markdown file
        files = list_markdown_files(target_path, self.category)
        if filename and not self.category:
            matching_files = [
                (cat, f) for cat, f in files 
                if f.lower() == filename.lower() or 
                   f.lower() == f"{filename.lower()}.md"
            ]
            
            if not matching_files:
                print(f"No file matching '{filename}' found")
                return 1
            elif len(matching_files) == 1:
                category, filename = matching_files[0]
            else:
                print(f"Multiple files matching '{filename}':")
                category, filename = select_file_interactive(matching_files)
        elif filename and self.category:
            file_path = target_path / self.category / f"{filename.replace('.md', '')}.md"
            if not file_path.exists():
                print(f"File '{filename}' not found in category '{self.category}'")
                return 1
            category = self.category
        else:
            if not files:
                print("No markdown files found")
                return 1
            category, filename = select_file_interactive(files)
        
        # Get full path to markdown file
        if category:
            md_file = target_path / category / filename
        else:
            md_file = target_path / filename
        
        # Confirm deletion
        if not self.force:
            confirm = input(f"Are you sure you want to delete '{md_file}'? [y/N] ").strip().lower()
            if confirm != 'y':
                print("Deletion cancelled")
                return 0
        
        # Delete the file
        try:
            os.remove(md_file)
            print(f"Deleted file: {md_file}")
            
            # Optionally remove empty parent directories
            if category:
                self._remove_empty_parents(md_file.parent, target_path)
                
            return 0
        except OSError as e:
            print(f"Error deleting file: {e}")
            return 1
    
    def _remove_empty_parents(self, directory: Path, stop_at: Path):
        """Remove empty parent directories up to stop_at path"""
        try:
            while directory != stop_at and directory != stop_at.parent:
                if not any(directory.iterdir()):  # Check if directory is empty
                    os.rmdir(directory)
                    print(f"Removed empty directory: {directory}")
                    directory = directory.parent
                else:
                    break
        except OSError as e:
            print(f"Note: Could not remove directories: {e}")
