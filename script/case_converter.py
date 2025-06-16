import argparse
import re
from typing import Callable

class CaseConverter:
    @staticmethod
    def camel_to_snake(name: str) -> str:
        s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
        return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

    @staticmethod
    def snake_to_camel(name: str) -> str:
        return ''.join(word.title() for word in name.split('_'))

    @staticmethod
    def snake_to_kebab(name: str) -> str:
        return name.replace('_', '-')

    @staticmethod
    def kebab_to_snake(name: str) -> str:
        return name.replace('-', '_')

    @staticmethod
    def camel_to_kebab(name: str) -> str:
        snake = CaseConverter.camel_to_snake(name)
        return CaseConverter.snake_to_kebab(snake)

    @staticmethod
    def kebab_to_camel(name: str) -> str:
        snake = CaseConverter.kebab_to_snake(name)
        return CaseConverter.snake_to_camel(snake)

    @staticmethod
    def get_converter(from_case: str, to_case: str) -> Callable[[str], str]:
        method_name = f"{from_case}_to_{to_case}"
        converter = getattr(CaseConverter, method_name, None)
        if not converter:
            raise ValueError(f"Unsupported conversion: {from_case} to {to_case}")
        return converter

def detect_case_type(name: str) -> str:
    if '_' in name:
        return 'snake'
    elif '-' in name:
        return 'kebab'
    elif name != name.lower() and name != name.upper() and '_' not in name and '-' not in name:
        return 'camel'
    else:
        return 'unknown'

def main():
    parser = argparse.ArgumentParser(description='Convert between different naming conventions')
    parser.add_argument('name', type=str, help='Name to convert')
    parser.add_argument('--from', dest='from_case', type=str, 
                       choices=['auto', 'camel', 'snake', 'kebab'],
                       default='auto', help='Source case type (default: auto-detect)')
    parser.add_argument('--to', type=str, required=True,
                       choices=['camel', 'snake', 'kebab'],
                       help='Target case type')
    
    args = parser.parse_args()
    
    # Determine source case type
    from_case = args.from_case
    if from_case == 'auto':
        from_case = detect_case_type(args.name)
        if from_case == 'unknown':
            raise ValueError(f"Could not auto-detect case type for: {args.name}")

    try:
        converter = CaseConverter.get_converter(from_case, args.to)
        result = converter(args.name)
        print(result)
    except ValueError as e:
        print(f"Error: {str(e)}")
        print("Available conversions:")
        print("- camel ↔ snake ↔ kebab")

if __name__ == '__main__':
    main()