import pyperclip

class FormFill:
    def __init__(self, template):
        self.template = template
        self.fields = {}
        self.lists = {}
        self.file_lists = {}

    def fill_field(self, key, value):
        self.fields[key] = value

    def fill_list(self, key, items):
        self.lists[key] = items

    def fill_files(self, key, file_paths, encoding='utf-8'):
        file_contents = []
        for path in file_paths:
            with open(path, 'r', encoding=encoding) as f:
                file_contents.append(f.read())
        self.file_lists[key] = file_contents

    def get_result(self):
        result = self.template
        
        for key, value in self.fields.items():
            result = result.replace(f'<{key}>', value)
            
        for key, items in self.lists.items():
            list_content = '\n'.join(f'- {item}' for item in items)
            result = result.replace(f'[{key}]', list_content)
            
        for key, contents in self.file_lists.items():
            code_blocks = '\n\n'.join(f'```python\n{content}\n```' for content in contents)
            result = result.replace(f'${key}$', code_blocks)
            
        return result

    def copy_to_clipboard(self):
        pyperclip.copy(self.get_result())

    def save_to_file(self, path, encoding='utf-8'):
        with open(path, 'w', encoding=encoding) as f:
            f.write(self.get_result())