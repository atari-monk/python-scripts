import argparse
from pathlib import Path
import re
from tool.form_fill.form_fill import FormFill

def main():
    parser = argparse.ArgumentParser(description='Fill template with data')
    parser.add_argument('template', type=Path, help='Path to template file')
    parser.add_argument('--output', type=Path, help='Path to output file (optional)')
    parser.add_argument('--encoding', default='utf-8', help='File encoding to use (default: utf-8)')
    
    args = parser.parse_args()
    
    try:
        with open(args.template, 'r', encoding=args.encoding) as f:
            template = f.read()
    except UnicodeDecodeError as e:
        print(f"Error reading template file: {e}")
        print("Try specifying a different encoding with --encoding parameter")
        return

    filler = FormFill(template)
    
    field_pattern = re.compile(r'<([^>]+)>')
    list_pattern = re.compile(r'\[([^\]]+)\]')
    file_pattern = re.compile(r'\$([^\$]+)\$')
    
    fields = set(field_pattern.findall(template))
    lists = set(list_pattern.findall(template))
    file_lists = set(file_pattern.findall(template))
    
    for field in fields:
        value = input(f'Enter value for {field}: ')
        filler.fill_field(field, value)
    
    for list_key in lists:
        print(f'Enter items for {list_key} (empty line to finish):')
        items = []
        while True:
            item = input('> ')
            if not item:
                break
            items.append(item)
        filler.fill_list(list_key, items)
    
    for file_key in file_lists:
        print(f'Enter file paths for {file_key} (empty line to finish):')
        paths = []
        while True:
            path = input('> ')
            if not path:
                break
            paths.append(path)
        
        filler.fill_files(file_key, paths, encoding=args.encoding)
    
    filler.copy_to_clipboard()
    print('\nResult copied to clipboard!\n')
    
    if args.output:
        try:
            filler.save_to_file(args.output, encoding=args.encoding)
            print(f'\nAlso saved to {args.output}')
        except UnicodeEncodeError as e:
            print(f"Error saving output file: {e}")
            print("Try specifying a different encoding with --encoding parameter")

if __name__ == '__main__':
    main()