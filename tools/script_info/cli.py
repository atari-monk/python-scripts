import argparse
from pathlib import Path
from tools.script_info.script_info import ScriptInfo

DEFAULT_SCRIPT_FILE = Path(r"C:\atari-monk\code\apps-data-store\scripts.json")

def main():
    parser = argparse.ArgumentParser(description="Manage CLI script information")
    subparsers = parser.add_subparsers(dest="command", required=True)

    list_parser = subparsers.add_parser("list", help="List all scripts")
    list_parser.add_argument(
        "--file", 
        type=Path, 
        help=f"JSON config file path (default: {DEFAULT_SCRIPT_FILE})",
        default=DEFAULT_SCRIPT_FILE,
        required=False
    )

    subparsers.add_parser("console", help="List available console scripts")

    args = parser.parse_args()

    if args.command == "list":
        try:
            if not args.file.exists():
                raise ValueError(f"File not found: {args.file}")
                
            scripts = ScriptInfo.load_from_file(args.file)
            print("\nRegistered Scripts:\n")
            print(ScriptInfo.format_list(scripts) + "\n")
        except ValueError as e:
            print(f"Error: {e}")
    elif args.command == "console":
        print("Available Console Scripts:")
        for script in ScriptInfo.get_console_scripts():
            print(f"  {script}")

if __name__ == "__main__":
    main()