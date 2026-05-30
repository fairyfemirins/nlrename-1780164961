import os
import pytest
from datetime import datetime
from unittest.mock import patch
from nlrename import parse_pattern, cli, apply_rename_ops


def test_parse_pattern_date():
    with patch('nlrename.datetime') as mock_datetime:
        mock_datetime.now.return_value = datetime(2026, 5, 30)
        assert parse_pattern("today's date") == [('prepend', '2026-05-30')]


def test_parse_pattern_case():
    assert parse_pattern("all to lowercase") == [('case', 'lower')]
    assert parse_pattern("all to uppercase") == [('case', 'upper')]


def test_parse_pattern_replace():
    assert parse_pattern("replace 'old' with 'new'") == [('replace', ("'old'", "'new'"))]


def test_apply_rename_ops():
    assert apply_rename_ops("file.txt", [('case', 'lower')]) == "file.txt"
    assert apply_rename_ops("FILE.TXT", [('case', 'lower')]) == "file.txt"
    assert apply_rename_ops("file.txt", [('prepend', '2026-05-30')]) == "2026-05-30_file.txt"
    assert apply_rename_ops("old_file.txt", [('replace', ('old', 'new'))]) == "new_file.txt"


def test_integration(tmp_path):
    test_file = tmp_path / "OLD_FILE.TXT"
    test_file.write_text("test")
    
    # Simulate CLI call
    os.chdir(tmp_path)
    from click.testing import CliRunner
    
    runner = CliRunner()
    result = runner.invoke(cli, ["all to lowercase", "OLD_FILE.TXT"])
    assert result.exit_code == 0
    assert (tmp_path / "old_file.txt").exists()