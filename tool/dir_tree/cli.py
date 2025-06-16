import argparse
import pyperclip
from pathlib import Path
from tool.dir_tree.directory_tree import DirectoryTree

def main():
    parser = argparse.ArgumentParser(description="Generate directory tree")
    parser.add_argument("path", help="Root directory path")
    parser.add_argument("-s", "--save", action="store_true", help="Save to file")
    parser.add_argument("-o", "--output", default="docs", help="Output directory")
    args = parser.parse_args()

    try:
        tree = DirectoryTree(args.path).generate()
        pyperclip.copy(tree)
        print("Tree copied to clipboard!")
        
        if args.save:
            output_dir = Path(args.path) / args.output
            output_dir.mkdir(exist_ok=True)
            output_file = output_dir / f"{Path(args.path).name}_tree.md"
            output_file.write_text(tree)
            print(f"Saved to {output_file}")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()