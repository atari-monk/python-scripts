#!/usr/bin/env python3
import argparse
from pathlib import Path
from tool.dev_blog_post.dev_blog_post import DevBlogPost

def main():
    parser = argparse.ArgumentParser(description='Store dev blog posts from clipboard')
    parser.add_argument('--init', action='store_true', help='Initialize configuration')
    parser.add_argument('--content', help='Set content folder name')
    parser.add_argument('--category', help='Set category name')
    parser.add_argument('--repo', help='Set repository path')
    parser.add_argument('--config', help='Custom config file path', type=valid_config_file,
                   default='C:\\atari-monk\\code\\dev-data\\blog_config.json')
    
    args = parser.parse_args()
    
    blog = DevBlogPost(config_path=args.config)
    
    if args.init or not blog.config.get("repo_path"):
        blog.config["repo_path"] = args.repo or input("Enter repository path: ")
        blog.save_config()
    
    if args.content:
        blog.config["current_content"] = args.content
        blog.save_config()
    
    if args.category:
        blog.config["current_category"] = args.category
        blog.save_config()
    
    try:
        saved_path = blog.process_clipboard_content()
        print(f"Post saved to: {saved_path}")
    except ValueError as e:
        print(f"Error: {e}")

def valid_config_file(path: str) -> Path:
    path_obj = Path(path)
    if not path_obj.is_file():
        raise argparse.ArgumentTypeError(f"Config file '{path_obj}' does not exist")
    return path_obj

if __name__ == "__main__":
    main()