import tempfile
import os
from tools.form_fill.form_fill import FormFill

class TestFormFill:
    def test_replace_single_field(self):
        template = "Hello <name>"
        filler = FormFill(template)
        filler.fill_field("name", "World")
        assert filler.get_result() == "Hello World"

    def test_replace_multiple_fields(self):
        template = "<greeting>, <name>!"
        filler = FormFill(template)
        filler.fill_field("greeting", "Hello")
        filler.fill_field("name", "World")
        assert filler.get_result() == "Hello, World!"

    def test_fill_list(self):
        template = "Items:\n[items]"
        filler = FormFill(template)
        filler.fill_list("items", ["apple", "banana", "cherry"])
        assert filler.get_result() == "Items:\n- apple\n- banana\n- cherry"

    def test_fill_file_list(self):
        template = "Code:\n$files$"
        with tempfile.NamedTemporaryFile(delete=False) as f1, tempfile.NamedTemporaryFile(delete=False) as f2:
            f1.write(b"print('hello')")
            f2.write(b"x = 42")
            f1.close()
            f2.close()
            
            filler = FormFill(template)
            filler.fill_files("files", [f1.name, f2.name])
            result = filler.get_result()
            
            assert "```python\nprint('hello')\n```" in result
            assert "```python\nx = 42\n```" in result
            
            os.unlink(f1.name)
            os.unlink(f2.name)

    def test_combined_replacements(self):
        template = "# <title>\n\n<description>\n\nFeatures:\n[features]\n\nCode examples:\n$code$"
        filler = FormFill(template)
        filler.fill_field("title", "My Script")
        filler.fill_field("description", "A useful script")
        filler.fill_list("features", ["Fast", "Reliable", "Simple"])
        
        with tempfile.NamedTemporaryFile(delete=False) as f:
            f.write(b"def main():\n    pass")
            f.close()
            
            filler.fill_files("code", [f.name])
            result = filler.get_result()
            
            assert "# My Script" in result
            assert "A useful script" in result
            assert "- Fast" in result
            assert "- Reliable" in result
            assert "- Simple" in result
            assert "```python\ndef main():\n    pass\n```" in result
            
            os.unlink(f.name)