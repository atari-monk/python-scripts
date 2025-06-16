#!/usr/bin/env python3
import argparse
from tool.dev_blog_index.dev_blog_index import DevBlogIndex

def main():
    parser = argparse.ArgumentParser(description='Generate index.md files for dev blog structure')
    parser.add_argument('--path', type=str, default=r'C:\atari-monk\code\dev-blog\content', help='Root directory of the blog')
    args = parser.parse_args()

    generator = DevBlogIndex(args.path)
    generator.generate()

if __name__ == '__main__':
    main()