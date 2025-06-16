import logging
import sys
import argparse
from tool.folder_indexer.folder_indexer import FolderIndexer
from tool.folder_indexer.simple_indexer import SimpleFolderIndexer

def main():
    parser = argparse.ArgumentParser(description='Generate documentation index.md')
    parser.add_argument('path', help='Path to directory')
    parser.add_argument('--list', '-l', action='store_true', help='Use simple indexer')

    args = parser.parse_args()

    if args.list:
        indexer = SimpleFolderIndexer(args.path)
    else:
        logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
        logger = logging.getLogger(__name__)
        indexer = FolderIndexer(args.path, logger)

    indexer.generate()

if __name__ == '__main__':
    sys.exit(main())