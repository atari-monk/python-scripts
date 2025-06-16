import pytest
import json
from tool.script_info.script_info import ScriptInfo


def test_valid_script_info():
    script = ScriptInfo(ScriptName="test_script", Description="Test description")
    assert script.ScriptName == "test_script"
    assert script.Description == "Test description"


def test_invalid_script_name():
    with pytest.raises(ValueError):
        ScriptInfo(ScriptName="InvalidScript", Description="Valid")
    with pytest.raises(ValueError):
        ScriptInfo(ScriptName="x"*31, Description="Valid")
    with pytest.raises(ValueError):
        ScriptInfo(ScriptName="script-with-dash", Description="Valid")


def test_load_from_file(tmp_path):
    file_path = tmp_path / "test.json"
    file_path.write_text(json.dumps([{"ScriptName": "load", "Description": "Loading test"}]))
    loaded = ScriptInfo.load_from_file(file_path)
    assert len(loaded) == 1
    assert loaded[0].ScriptName == "load"


def test_format_list():
    scripts = [ScriptInfo(ScriptName="print", Description="Print test")]
    output = ScriptInfo.format_list(scripts)
    assert "print : Print test" in output