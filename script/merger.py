import argparse
import os
import sys
from typing import List, Set, Optional

DEFAULT_MERGED_NAME = "merged"
ALLOWED_EXTENSIONS = {'txt', 'md', 'py', 'json', 'toml'}
IGNORED_DIRS = {".git", "node_modules", "__pycache__", "venv", "dist", "build", "target"}
IGNORED_FILES = {f"{DEFAULT_MERGED_NAME}.{ext}" for ext in ALLOWED_EXTENSIONS}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

class FileMerger:
    def __init__(self):
        self.file_count = 0
        self.total_size = 0
        self.skipped_files = 0

    def get_files_to_merge(self, directory: str, extensions: Optional[Set[str]] = None) -> List[str]:
        """Scan directory for files to merge, with optional extension filtering."""
        file_paths = []
        for root, dirs, files in os.walk(directory):
            dirs[:] = [d for d in dirs if d not in IGNORED_DIRS]
            
            for file in files:
                if file in IGNORED_FILES:
                    continue
                
                file_path = os.path.join(root, file)
                try:
                    file_size = os.path.getsize(file_path)
                    if file_size > MAX_FILE_SIZE:
                        print(f"Warning: Skipping large file {file_path} ({file_size/1024:.1f}KB)")
                        self.skipped_files += 1
                        continue

                    if extensions and not any(file.endswith(ext) for ext in extensions):
                        continue

                    file_paths.append(file_path)
                    self.file_count += 1
                    self.total_size += file_size
                except OSError as e:
                    print(f"Warning: Could not access {file_path}: {e}")
                    self.skipped_files += 1
        
        return sorted(file_paths)

    def write_merged_file(self, file_paths: List[str], output_path: str, extension: str) -> bool:
        """Write merged content to output file with appropriate formatting."""
        try:
            with open(output_path, 'w', encoding='utf-8') as outfile:
                # Write header
                outfile.write(self._get_file_header(extension))
                
                for file_path in file_paths:
                    rel_path = os.path.relpath(file_path, os.path.dirname(output_path))
                    outfile.write(self._get_file_header(extension, rel_path))
                    
                    try:
                        with open(file_path, 'r', encoding='utf-8') as infile:
                            content = infile.read()
                            outfile.write(content)
                    except UnicodeDecodeError:
                        outfile.write(f"\n\n[Binary file content omitted]\n\n")
                    except Exception as e:
                        outfile.write(f"\n\nError reading file: {e}\n\n")
                    
                    outfile.write(self._get_file_footer(extension))
            
            # Add summary at the end
            with open(output_path, 'a', encoding='utf-8') as outfile:
                outfile.write(self._get_summary_footer(extension))
            return True
        except Exception as e:
            print(f"Error writing output file: {e}", file=sys.stderr)
            return False

    def _get_file_header(self, extension: str, filename: str = "") -> str:
        """Generate appropriate header for each file based on output format."""
        if extension == 'md':
            return f"### {filename}\n\n```\n" if filename else "# Merged Files\n\n"
        elif extension == 'py':
            return f"# File: {filename}\n{'#' * 80}\n" if filename else "# Merged Files\n"
        elif extension == 'json':
            return ""  # JSON format needs special handling
        elif extension == 'toml':
            return f"# {filename}\n{'#' * 80}\n" if filename else "# Merged TOML Files\n"
        else:  # txt
            return f"{filename}\n{'-'*80}\n" if filename else "Merged Files\n=============\n\n"

    def _get_file_footer(self, extension: str) -> str:
        """Generate appropriate footer for each file based on output format."""
        if extension == 'md':
            return "\n```\n\n"
        elif extension == 'py':
            return "\n\n# " + "=" * 77 + "\n\n"
        elif extension == 'json':
            return ""  # JSON format needs special handling
        elif extension == 'toml':
            return "\n\n" + "#" * 80 + "\n\n"
        else:  # txt
            return "\n\n"

    def _get_summary_footer(self, extension: str) -> str:
        """Generate summary footer with merge statistics."""
        summary = f"\n\nMerged {self.file_count} files"
        if self.skipped_files > 0:
            summary += f" (skipped {self.skipped_files} files)"
        
        if extension == 'md':
            return f"\n\n---\n\n*{summary}*\n"
        elif extension == 'py':
            return f"\n\n# {summary.replace('(', '# (').replace(')', '#)')}\n"
        elif extension == 'toml':
            return f"\n\n# {summary}\n"
        else:  # txt and others
            return f"\n\n{summary}\n"

def main():
    parser = argparse.ArgumentParser(
        description='Merge files from a directory into a single file with optional filtering.',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument('path', type=str, help='Directory containing files to merge')
    parser.add_argument('--ext', choices=ALLOWED_EXTENSIONS, default='txt',
                       help='Output file extension')
    parser.add_argument('--output', type=str, help='Custom output file path')
    parser.add_argument('--name', type=str, default=DEFAULT_MERGED_NAME,
                       help='Base name for output file')
    parser.add_argument('--filter', type=str, nargs='+',
                       help='Only include files with these extensions (e.g., .py .js)')
    parser.add_argument('--no-summary', action='store_true',
                       help='Omit summary information from output')
    parser.add_argument('--verbose', action='store_true',
                       help='Show detailed progress information')

    args = parser.parse_args()

    # Validate path
    if not os.path.isdir(args.path):
        print(f"Error: {args.path} is not a valid directory", file=sys.stderr)
        sys.exit(1)

    merger = FileMerger()
    
    # Get files to merge with optional extension filtering
    extensions = {ext.lower() for ext in args.filter} if args.filter else None
    file_paths = merger.get_files_to_merge(args.path, extensions)
    
    if not file_paths:
        print("No files found to merge", file=sys.stderr)
        sys.exit(1)

    # Determine output path
    if args.output:
        output_path = args.output
    else:
        output_path = os.path.join(args.path, f"{args.name}.{args.ext}")

    if args.verbose:
        print(f"Found {merger.file_count} files to merge")
        if merger.skipped_files > 0:
            print(f"Skipped {merger.skipped_files} files")
        print(f"Output will be saved to: {output_path}")

    # Write merged file
    if not merger.write_merged_file(file_paths, output_path, args.ext):
        sys.exit(1)

    print(f"Successfully merged {merger.file_count} files to {output_path}")
    if merger.skipped_files > 0:
        print(f"Note: Skipped {merger.skipped_files} files")

if __name__ == "__main__":
    main()